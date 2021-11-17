from gpiozero import Button, LED
import RPi.GPIO as GPIO
import time

btoOlhoPequeno = Button(2)
ledOlhoPequeno = LED(17)
btoOlhoMedio = Button(3)
ledOlhoMedio = LED(27)
btoOlhoGrande = Button(4)
ledOlhoGrande = LED(22)
tipoOlho = "nenhum"

def pisca():
    ledOlhoPequeno.on()
    ledOlhoMedio.on()
    ledOlhoGrande.on()
    time.sleep(0.20)
    ledOlhoPequeno.off()
    ledOlhoMedio.off()
    ledOlhoGrande.off()
    time.sleep(0.20)

def selecionaOlho():
    while tipoOlho == "nenhum":
        if btoOlhoPequeno.is_pressed:
            tipoOlho = "pequeno"
            ledOlhoPequeno.on()
            return tipoOlho
        if btoOlhoMedio.is_pressed:
            tipoOlho = "medio"
            ledOlhoMedio.on()
            return tipoOlho
        if btoOlhoGrande.is_pressed:
            tipoOlho = "grande"
            ledOlhoGrande.on()
            return tipoOlho
        if tipoOlho == "nenhum":
            pisca()
            

