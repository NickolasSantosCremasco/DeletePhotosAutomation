import xml.etree.ElementTree as ET
import re


def ler_xml():
    tree = ET.parse("window_dump.xml")
    return tree.getroot()


def pegar_bounds(node):
    bounds = node.attrib.get("bounds")
    if not bounds:
        return None

    nums = list(map(int, re.findall(r'\d+', bounds)))

    x = (nums[0] + nums[2]) // 2
    y = (nums[1] + nums[3]) // 2

    return x, y

def encontrar_por_resource_id(root, rid):

    for node in root.iter():

        if node.attrib.get("resource-id") == rid:

            coords = pegar_bounds(node)

            if coords:
                return coords

    return None



def pegar_textos(root):

    textos = []

    for node in root.iter():

        texto = node.attrib.get("text")

        if texto:
            textos.append(texto)

    return textos


def detectar_albuns(root, comodos):

    resultados = []

    for node in root.iter():

        texto = node.attrib.get("text")

        if texto in comodos:

            coords = pegar_bounds(node)

            if coords:
                resultados.append((texto, coords[0], coords[1]))

    return resultados

def elemento_existe(root, texto):

    for node in root.iter():

        if node.attrib.get("text") == texto:
            return True

    return False