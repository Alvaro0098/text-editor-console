from typing import List
from .component_main import ComponenteDocumento
from .parrafo import Parrafo 


class Pagina(ComponenteDocumento):
    """Compuesto (Composite) - Contiene párrafos (Leaf o Composite)."""
    
    def __init__(self):
        self.hijos: List[Parrafo] = []

    def agregar_parrafo(self, parrafo: Parrafo):
        """Método de gestión: añade un Parrafo a la Página."""
        self.hijos.append(parrafo)

    def contar_palabras(self) -> int:
        """Operación: Delega la acción a todos los Parrafos hijos y suma los resultados."""
        return sum(hijo.contar_palabras() for hijo in self.hijos)

    def mostrar(self) -> str:
        """
        Operación: Muestra el contenido de la Página.
        Delega la acción a cada Parrafo hijo y los une con un doble salto de línea ('\n\n').
        """
        return "\n\n".join(hijo.mostrar() for hijo in self.hijos)