import time

from actions import tap, swipe, dump_ui, selecionar_tudo, mover_lixeira, confirmar_exclusao, voltar, limpar_notificacoes
from config import BOTOES, COMODOS
from detector import ler_xml, detectar_albuns, pegar_textos, elemento_existe, encontrar_por_resource_id

CHECKMARK_ID = "com.google.android.apps.photos:id/end_checkmark"


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

def clicar_selecionar_tudo():

    dump_ui()
    root = ler_xml()

    coords = encontrar_por_resource_id(root, CHECKMARK_ID)

    if coords:

        print("Botão selecionar encontrado:", coords)
        tap(*coords)
        time.sleep(1)
        return True

    print("Botão selecionar não encontrado")
    return False


def limpar_album(nome):

    print('Verificando se tem Notificações')
    limpar_notificacoes()

    dump_ui()
    root = ler_xml()

    coords = encontrar_album_por_nome(root, nome)

    # ✅ CORREÇÃO 1: retorno explícito
    if not coords:
        print("Álbum não encontrado na tela:", nome)
        return False

    tap(*coords)
    # ✅ CORREÇÃO 2: valida entrada no álbum corretamente
    time.sleep(1)

    dump_ui()
    root = ler_xml()

    # Se não encontrou botão de seleção nem indicador de vazio → erro de navegação
    if not encontrar_por_resource_id(root, CHECKMARK_ID) and not elemento_existe(root, "Nenhum item"):
        print("Falha ao entrar no álbum")
        voltar()
        return False

    print('Verificando se tem Notificações')
    limpar_notificacoes()

    if not clicar_selecionar_tudo():

        print("Não consegui encontrar botão de seleção")

        dump_ui()
        root = ler_xml()

        # ✅ CORREÇÃO 3: tratamento correto de álbum vazio
        if elemento_existe(root, "Nenhum item"):
            print("Álbum vazio")
            voltar()
            return True

        # tentativa de retry
        print("Tentando novamente...")
        time.sleep(1)

        if not clicar_selecionar_tudo():
            print("Falha real → voltando")
            voltar()
            return False

        # ✅ CORREÇÃO 4: se funcionou no retry, continua fluxo
        print("Retry funcionou, continuando...")

    mover_lixeira()
    confirmar_exclusao()
    voltar()

    # ✅ CORREÇÃO 5: espera real de exclusão
    if not esperar_exclusao_finalizar():
        print("Exclusão não terminou corretamente")

    voltar()

    # ✅ CORREÇÃO 6: agora sim usar esperar_elemento (lista de álbuns)
    if not esperar_elemento():
        print("Tela de álbuns não carregou corretamente")
        return False

    # ✅ CORREÇÃO 7: retorno final obrigatório
    return True

def tela_pronta_para_excluir():

    dump_ui()

    root = ler_xml()

    return elemento_existe(root, "Selecionar tudo")

def encontrar_album_por_nome(root, nome):

    for node in root.iter():

        texto = node.attrib.get("text")

        if texto == nome:

            bounds = node.attrib.get("bounds")

            if bounds:

                import re

                nums = list(map(int, re.findall(r'\d+', bounds)))

                x = (nums[0] + nums[2]) // 2
                y = (nums[1] + nums[3]) // 2

                return x, y

    return None

def esperar_elemento(tentativas=5):

    for _ in range(tentativas):

        dump_ui()
        root = ler_xml()

        albuns = detectar_albuns(root, COMODOS)

        if albuns:
            return True

        time.sleep(1)

    return False

def esperar_exclusao_finalizar(tentativas=10):

    for _ in range(tentativas):

        dump_ui()
        root = ler_xml()

        if not encontrar_por_resource_id(root, CHECKMARK_ID):
            return True

        time.sleep(1)

    return False

def escanear_albuns():

    vistos = set()

    sem_novos = 0
    while True:

        limpar_notificacoes()

        dump_ui()

        root = ler_xml()

        albuns = detectar_albuns(root, COMODOS)

        novos = 0

        for nome, x, y in albuns:

            chave = nome

            if chave in vistos:
                continue

            vistos.add(chave)

            print("Processando:", nome)

            limpar_album(nome)

            novos += 1

            # voltar para lista de álbuns
            time.sleep(2)

            # atualizar tela após voltar
            dump_ui()
            root = ler_xml()

        if novos == 0:
            sem_novos += 1
        else:
            sem_novos = 0

        if sem_novos >= 3:
            print("\nFim da lista.")
            break

        swipe(500, 2000, 500, 800)

        time.sleep(2)

