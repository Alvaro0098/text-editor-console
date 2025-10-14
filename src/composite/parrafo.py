# src/composite/parrafo.py

from .component_main import ComponentMain
from .linea import Linea

class Parrafo(ComponentMain):
    def __init__(self):
        self.hijos = []

    def agregar_linea(self, linea: Linea):

        self.hijos.append(linea)

    def contar_palabras(self):

        return sum(hijo.contar_palabras() for hijo in self.hijos)

    def contar_paginas(self):

        return 0

    def mostrar(self):

        return "\n".join(hijo.mostrar() for hijo in self.hijos)