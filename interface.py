from PySimpleGUI import PySimpleGUI as sg
import output as base64


#Layout da janela
sg.theme('Reddit')
layout = [
    [sg.Text('Escolha o par de olhos mais próximo do seu')],
    [sg.Button('', image_data=base64.Pequenos), 
     sg.Button('', image_data=base64.Medios), 
     sg.Button('', image_data=base64.Grandes)
    ]
]
#Janela
janela = sg.Window('', layout)

eye_value = None

while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
    if eventos == 'Olhos Pequenos':
        eye_value = 0.2
    elif eventos == 'Olhos Médios':
        eye_value = 0.3
    elif eventos == 'Olhos Grandes':
        eye_value = 0.4
    janela.close()

