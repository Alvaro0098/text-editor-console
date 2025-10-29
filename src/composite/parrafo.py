from typing import List
from .component_main import ComponenteDocumento 
from .linea import Linea 
from .palabra import Palabra 
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
        """Extrae todas las Palabras del Parrafo que contienen texto."""
        palabras_secuenciales: List[Palabra] = []
        for linea in self.hijos:
            for palabra in linea.hijos:

                if palabra.texto: 
                    palabras_secuenciales.append(palabra)
        return palabras_secuenciales
    
    
    def aplicar_reflow(self, ancho_linea: int):
        """Reconstruye la estructura de Líneas para ajustarse al ancho_linea sin cortar palabras."""
        
        todas_las_palabras = self._obtener_todas_las_palabras()
        self.hijos.clear() 

        if not todas_las_palabras:
            linea_inicial = Linea(ancho=ancho_linea)
            self.hijos.append(linea_inicial)
            linea_inicial.hijos.append(Palabra(""))
            return

        linea_actual = Linea(ancho=ancho_linea)
        self.hijos.append(linea_actual)
        longitud_actual_linea = 0
        
        for palabra in todas_las_palabras:
            longitud_palabra = len(palabra.texto)
            espacio_requerido = 1 if longitud_actual_linea > 0 else 0
            
            if longitud_actual_linea + espacio_requerido + longitud_palabra > ancho_linea:
                linea_actual = Linea(ancho=ancho_linea)
                self.hijos.append(linea_actual)
                linea_actual.hijos.append(palabra)
                longitud_actual_linea = longitud_palabra
            else:
                linea_actual.hijos.append(palabra)
                longitud_actual_linea += espacio_requerido + longitud_palabra


        if longitud_actual_linea == ancho_linea:

            nueva_linea_cursor = Linea(ancho=ancho_linea)
            self.hijos.append(nueva_linea_cursor)
            nueva_linea_cursor.hijos.append(Palabra(""))
        

        elif longitud_actual_linea < ancho_linea:
            linea_actual.hijos.append(Palabra(""))