# composite/pagina.py

# 1. Necesario para las anotaciones de tipo List
from typing import List

# 2. Asumimos que ComponenteDocumento es la clase base (el Componente)
# y que se encuentra en un módulo dentro del mismo paquete.
from .component_main import ComponenteDocumento

# 3. Necesitamos importar Parrafo para las anotaciones de tipo,
# ya que Pagina lo contiene. Asumimos que está en el mismo paquete.
from .parrafo import Parrafo 
# Nota: Si Parrafo no existe aún, tendrás que crearlo como otro 'Componente'
# (posiblemente otro Composite, o un Leaf si contiene Linea/Palabra).

class Pagina(ComponenteDocumento):
    """Compuesto (Composite) - Contiene párrafos (Leaf o Composite)."""
    
    def __init__(self):
        # La lista de hijos (los Parrafos)
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