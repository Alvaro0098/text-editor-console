# src/composite/parrafo.py

from typing import List
from .component_main import ComponenteDocumento 
from .linea import Linea 
# Importamos la interfaz de Strategy para tipar el método de alineación
from ..strategy.alineacion_strategy import IStrategyAlineacion 

class Parrafo(ComponenteDocumento):
    """Compuesto (Composite) - Contiene líneas y gestiona el 'reflow' de palabras."""
    def __init__(self):
        self.hijos: List[Linea] = []

    def agregar_linea(self, linea: Linea):
        self.hijos.append(linea)

    def contar_palabras(self) -> int:
        return sum(hijo.contar_palabras() for hijo in self.hijos)

    def mostrar(self) -> str:
        """Responsabilidad: Unir las líneas, añadiendo un salto de línea entre ellas."""
        return "\n".join(hijo.mostrar() for hijo in self.hijos)
    
    # 🚨 MÉTODO AÑADIDO (CORRECCIÓN) 🚨
    def cambiar_alineacion(self, nueva_alineacion: IStrategyAlineacion) -> None:
        """
        Responsabilidad (Strategy/Composite): Propaga la nueva estrategia de 
        alineación a todas las Líneas contenidas en el párrafo.
        """
        for linea in self.hijos:
            linea.cambiar_alineacion(nueva_alineacion)
    
    def aplicar_reflow(self, ancho_linea: int):
        # Lógica de reajuste de palabras en líneas. (PENDIENTE CRÍTICO)
        pass