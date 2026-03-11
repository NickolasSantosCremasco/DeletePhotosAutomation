import time
from actions import tap
from config import BOTOES

def abrir_fotos():
    tap(*BOTOES["fotos"])
    time.sleep(2)

def abrir_albuns():
    tap(*BOTOES["albuns"])
    time.sleep(2)

def abrir_este_dispositivo():
    tap(*BOTOES["este_dispositivo"])
    time.sleep(2)

def navegar_para_dispositivo():
    abrir_fotos()
    abrir_albuns()
    abrir_este_dispositivo()