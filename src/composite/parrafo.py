# src/composite/parrafo.py

from typing import List
from .component_main import ComponenteDocumento 
from .linea import Linea 
from .palabra import Palabra # <-- Asegurarse de importar Palabra
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
    
    def cambiar_alineacion(self, nueva_alineacion: IStrategyAlineacion) -> None:
        """Propaga la nueva estrategia de alineación a todas las Líneas contenidas en el párrafo."""
        for linea in self.hijos:
            linea.cambiar_alineacion(nueva_alineacion)

    def _obtener_todas_las_palabras(self) -> List[Palabra]:
        """Extrae todas las Palabras del Parrafo en un orden secuencial."""
        palabras_secuenciales: List[Palabra] = []
        for linea in self.hijos:
            palabras_secuenciales.extend(linea.hijos)
        return palabras_secuenciales
    
    def aplicar_reflow(self, ancho_linea: int):
        """Reconstruye la estructura de Líneas para ajustarse al ancho_linea sin cortar palabras."""
        
        todas_las_palabras = self._obtener_todas_las_palabras()
        
        # Limpiamos las Líneas antiguas para reconstruir el párrafo
        self.hijos.clear() 
        
        if not todas_las_palabras:
            return

        linea_actual = Linea(ancho=ancho_linea)
        self.hijos.append(linea_actual)
        longitud_actual_linea = 0
        
        for palabra in todas_las_palabras:
            longitud_palabra = len(palabra.texto)
            
            # Espacio requerido (si no es la primera palabra de la línea)
            espacio_requerido = 1 if longitud_actual_linea > 0 else 0
            
            # Condición de Salto de Línea
            if longitud_actual_linea + espacio_requerido + longitud_palabra > ancho_linea:
                
                # Crear nueva Línea e iniciarla con la Palabra actual
                linea_actual = Linea(ancho=ancho_linea)
                self.hijos.append(linea_actual)
                linea_actual.hijos.append(palabra)
                longitud_actual_linea = longitud_palabra
            else:
                # Añadir a la Línea actual
                linea_actual.hijos.append(palabra)
                longitud_actual_linea += espacio_requerido + longitud_palabra