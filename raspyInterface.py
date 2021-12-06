from gpiozero import Button, LED
import time

#definição dos pins
btoOlhoPequeno = Button(2)
ledOlhoPequeno = LED(17)
btoOlhoMedio = Button(3)
ledOlhoMedio = LED(27)
btoOlhoGrande = Button(4)
ledOlhoGrande = LED(22)

tipoOlho = "a"

#método para indicar que o usuário precisa
#selecionar um perfil
def pisca():
    ledOlhoPequeno.on()
    ledOlhoMedio.on()
    ledOlhoGrande.on()
    time.sleep(0.20)
    ledOlhoPequeno.off()
    ledOlhoMedio.off()
    ledOlhoGrande.off()
    time.sleep(0.20)

#quando o usuário selecionar um botão fisico,
#retorna o valor de abertura minima para o tipo do olho
def selecionaOlho():
    tipoOlho = "nenhum"
    while tipoOlho == "nenhum":
        if btoOlhoPequeno.is_pressed:
            tipoOlho = "pequeno"
            ledOlhoPequeno.on()
            return 0.18
        if btoOlhoMedio.is_pressed:
            tipoOlho = "medio"
            ledOlhoMedio.on()
            return 0.22
        if btoOlhoGrande.is_pressed:
            tipoOlho = "grande"
            ledOlhoGrande.on()
            return 0.26
        if tipoOlho == "nenhum":
            pisca()