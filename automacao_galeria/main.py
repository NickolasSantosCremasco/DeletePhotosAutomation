from automacao_galeria.detector import detectar_albuns
from navigation import navegar_para_dispositivo, escanear_albuns

def main():


    navegar_para_dispositivo()

    albuns = escanear_albuns()

    print("\nÁlbuns encontrados:")

    for nome in albuns:
        print(nome)


if __name__ == "__main__":
    main()