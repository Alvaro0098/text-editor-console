from .component_main import ComponentMain
from .parrafo import Parrafo

class Pagina(ComponentMain):
    def __init__(self):
        self.hijos = []

    def agregar_parrafo(self, parrafo: Parrafo):
        self.hijos.append(parrafo)

    def contar_palabras(self):
        return sum(hijo.contar_palabras() for hijo in self.hijos)

    def contar_paginas(self):
        return 1 + sum(hijo.contar_paginas() for hijo in self.hijos)

    def mostrar(self):
        return "\n\n".join(hijo.mostrar() for hijo in self.hijos)