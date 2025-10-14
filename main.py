# main.py

from src.composite.documento import Documento
from src.composite.pagina import Pagina
from src.composite.parrafo import Parrafo
from src.composite.linea import Linea
from src.composite.palabra import Palabra

def main():
    print("¡El editor de texto se ha iniciado correctamente!")
    print("-" * 30)


    palabra1 = Palabra("Hola")
    palabra2 = Palabra("mundo.")
    palabra3 = Palabra("Este")
    palabra4 = Palabra("es")
    palabra5 = Palabra("un")
    palabra6 = Palabra("ejemplo")
    palabra7 = Palabra("de")
    palabra8 = Palabra("la")
    palabra9 = Palabra("estructura.")


    linea1 = Linea()
    linea1.agregar_palabra(palabra1)
    linea1.agregar_palabra(palabra2)

    linea2 = Linea()
    linea2.agregar_palabra(palabra3)
    linea2.agregar_palabra(palabra4)
    linea2.agregar_palabra(palabra5)

    linea3 = Linea()
    linea3.agregar_palabra(palabra6)
    linea3.agregar_palabra(palabra7)
    linea3.agregar_palabra(palabra8)
    linea3.agregar_palabra(palabra9)


    parrafo1 = Parrafo()
    parrafo1.agregar_linea(linea1)
    parrafo1.agregar_linea(linea2)

    parrafo2 = Parrafo()
    parrafo2.agregar_linea(linea3)

    pagina1 = Pagina()
    pagina1.agregar_parrafo(parrafo1)

    pagina2 = Pagina()
    pagina2.agregar_parrafo(parrafo2)


    documento1 = Documento()
    documento1.agregar_pagina(pagina1)
    documento1.agregar_pagina(pagina2)


    print("Contenido del documento:")
    print(documento1.mostrar())
    print("-" * 30)
    print(f"Número total de palabras: {documento1.contar_palabras()}")
    print(f"Número total de páginas: {documento1.contar_paginas()}")

if __name__ == "__main__":
    main()