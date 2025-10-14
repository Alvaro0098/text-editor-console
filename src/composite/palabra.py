from .component_main import ComponentMain

class Palabra(ComponentMain):
    def __init__(self, texto: str):
        self.texto = texto

    def contar_palabras(self):
        return 1

    def contar_paginas(self):
        return 0

    def mostrar(self):
        return self.texto