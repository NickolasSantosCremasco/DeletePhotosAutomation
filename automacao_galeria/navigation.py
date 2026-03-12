import time

from actions import tap, swipe, dump_ui
from config import BOTOES, COMODOS
from detector import ler_xml, detectar_albuns, pegar_textos


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


def mostrar_textos():

    dump_ui()

    root = ler_xml()
    textos = pegar_textos(root)

    for t in textos:
        print(t)


def escanear_albuns():

    encontrados = {}
    tentativas = 0

    while tentativas < 10:

        dump_ui()

        root = ler_xml()

        albuns = detectar_albuns(root, COMODOS)

        for nome, x, y in albuns:

            if nome not in encontrados:

                encontrados[nome] = (x, y)
                print("Detectado:", nome)

        swipe(500, 2000, 500, 800)

        time.sleep(2)

        tentativas += 1

    return encontrados