# Código baseado no artigo do Adrian Rosebrock
# https://bit.ly/2CYC7Gf

# importar pacotes necessários
from scipy.spatial import distance as dist
from imutils import face_utils
from threading import Thread
import numpy as np
import imutils
import RPi.GPIO as GPIO
import time
import dlib
import cv2
import matplotlib.pyplot as plt
from picamera.array import PiRGBArray
from picamera import PiCamera
import raspyInterface

# definir constantes
buzzerPin = 21
GPIO.setup(buzzerPin,GPIO.OUT)
WEBCAM = 0
EYE_AR_THRESH = raspyInterface.selecionaOlho()
EYE_AR_CONSEC_FRAMES = 8
COUNTER = 0
ALARM_ON = False

def alarme():
    #Toca o buzzer
    GPIO.output(buzzerPin,GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(buzzerPin,GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(buzzerPin,GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(buzzerPin,GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(buzzerPin,GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(buzzerPin,GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(buzzerPin,GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(buzzerPin,GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(buzzerPin,GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(buzzerPin,GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(buzzerPin,GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(buzzerPin,GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(buzzerPin,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(buzzerPin,GPIO.LOW)
    time.sleep(2)

def eye_aspect_ratio(eye):
    # calculo das distancias entre 2 conjuntos de landmarks dos olhos vertical
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # calculo das distancias entre 2 conjuntos de landmarks dos olhos horizontal
    C = dist.euclidean(eye[0], eye[3])

    # calcula o EAR
    ear = (A + B) / (2.0 * C)

    # retorna o EAR
    return ear


# dlib's face detector (HOG-based)
print("[INFO] carregando o preditor de landmark...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# pegar os índices do previsor, para olhos esquerdo e direito
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# inicializar vídeo
print("[INFO] inicializando streaming de vídeo...")

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.5)

# loop sobre os frames do vídeo
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    image = frame.array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detectar faces (grayscale)
    rects = detector(gray, 0)

    # loop nas detecções de faces
    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # extrair coordenadas dos olhos e calcular a proporção de abertura
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        # ratio média para os dois olhos
        ear = (leftEAR + rightEAR) / 2.0

        # convex hull para os olhos
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(image, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(image, [rightEyeHull], -1, (0, 255, 0), 1)

        # checar ratio x threshold
        if ear < EYE_AR_THRESH:
            COUNTER += 1

            # dentro dos critérios, soar o alarme
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                # ligar alarme
                if not ALARM_ON:
                    ALARM_ON = True
                    t = Thread(target=alarme)
                    t.deamon = True
                    t.start()

                cv2.putText(image, "[ALERTA] FADIGA!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # caso acima do threshold, resetar o contador e desligar o alarme
        else:
            COUNTER = 0
            ALARM_ON = False

        # desenhar a proporção de abertura dos olhos
        cv2.putText(image, "EAR: {:.2f}".format(ear), (300, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # mostrar frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    
    #limpa memória
    rawCapture.truncate(0)