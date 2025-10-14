from .component_main import ComponentMain
from .pagina import Pagina

class Documento(ComponentMain):
    def __init__(self):
        self.hijos = []

    def agregar_pagina(self, pagina: Pagina):
        self.hijos.append(pagina)

    def contar_palabras(self):
        return sum(hijo.contar_palabras() for hijo in self.hijos)

    def contar_paginas(self):
        return sum(hijo.contar_paginas() for hijo in self.hijos)

    def mostrar(self):
        return "\n\n\n".join(hijo.mostrar() for hijo in self.hijos)