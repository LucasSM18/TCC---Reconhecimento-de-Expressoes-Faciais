from gpiozero import Button, LED
import time

btoOlhoPequeno = Button(2)
ledOlhoPequeno = LED(17)
btoOlhoMedio = Button(3)
ledOlhoMedio = LED(27)
btoOlhoGrande = Button(4)
ledOlhoGrande = LED(22)
btoAtivado = "nenhum"

def pisca():
    ledOlhoPequeno.on()
    ledOlhoMedio.on()
    ledOlhoGrande.on()
    time.sleep(0.20)
    ledOlhoPequeno.off()
    ledOlhoMedio.off()
    ledOlhoGrande.off()
    time.sleep(0.20)

while btoAtivado == "nenhum":
    if btoOlhoPequeno.is_pressed:
        btoAtivado = "pequeno"
        ledOlhoPequeno.on()
    if btoOlhoMedio.is_pressed:
        btoAtivado = "medio"
        ledOlhoMedio.on()
    if btoOlhoGrande.is_pressed:
        btoAtivado = "grande"
        ledOlhoGrande.on()
    if btoAtivado == "nenhum":
        pisca() 