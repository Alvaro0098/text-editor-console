from typing import List
from .pagina import Pagina # Para List[Pagina]
from .component_main import ComponenteDocumento
class Documento(ComponenteDocumento):
    """Compuesto (Composite) - Raíz de la jerarquía."""
    def __init__(self):
        self.hijos: List[Pagina] = []

    def agregar_pagina(self, pagina: Pagina):
        self.hijos.append(pagina)

    def contar_palabras(self) -> int:
        return sum(hijo.contar_palabras() for hijo in self.hijos)

    def mostrar(self) -> str:
        """Responsabilidad: Retorna la vista completa del documento (separando páginas)."""
        return "\n\n\n".join(hijo.mostrar() for hijo in self.hijos)

    def contar_paginas(self) -> int:
        """Responsabilidad: Genera una estadística, contando los elementos Pagina."""
        return len(self.hijos)