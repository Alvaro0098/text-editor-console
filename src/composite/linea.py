from .component_main import ComponentMain
from .palabra import Palabra

class Linea(ComponentMain):
    def __init__(self):
        self.hijos = []

    def agregar_palabra(self, palabra: Palabra):
        self.hijos.append(palabra)

    def contar_palabras(self):
        return sum(hijo.contar_palabras() for hijo in self.hijos)

    def contar_paginas(self):
        return 0

    def mostrar(self):
        return " ".join(hijo.mostrar() for hijo in self.hijos)