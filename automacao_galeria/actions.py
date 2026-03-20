import os
import time
from config import BOTOES


adb = r"C:\Users\Nickolas Cremasco\Dropbox\scrcpy-win64-v3.3.4\scrcpy-win64-v3.3.4\adb.exe"

def tap(x, y):
    os.system(f'"{adb}" shell input tap {x} {y}')

def dump_ui():
    os.system(f'"{adb}" shell uiautomator dump')
    os.system(f'"{adb}" pull /sdcard/window_dump.xml')

def swipe(x1, y1, x2, y2, tempo=300):
    os.system(f'"{adb}" shell input swipe {x1} {y1} {x2} {y2} {tempo}')

def selecionar_tudo():
    tap(*BOTOES["selecionar_tudo"])
    time.sleep(1)


def mover_lixeira():
    tap(*BOTOES["mover_para_lixeira"])
    time.sleep(1)


def confirmar_exclusao():
    tap(*BOTOES["confirmar"])
    time.sleep(2)


def esperar_elemento(nome, tentativas=5):

    for _ in range(tentativas):

        dump_ui()
        root = ler_xml()

        albuns = detectar_albuns(root, COMODOS)

        if albuns:
            return True

        time.sleep(1)

    return False


def voltar():
    tap(*BOTOES["voltar"])
    time.sleep(2)

def limpar_notificacoes():

    swipe(500, 200, 500, 0)