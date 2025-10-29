from typing import List
from src.composite.component_main import ComponenteDocumento
from src.composite.linea import Linea
from src.composite.palabra import Palabra
from src.strategy.alineacion_strategy import IStrategyAlineacion, AlineacionIzquierda 

class Parrafo(ComponenteDocumento):
    """
    Contenedor de líneas. Responsable de organizar el texto para que no se corten palabras
    y aplicar reflow.
    Patrón de Diseño: Composite (Component).
    Ítem de Cambio Oculto: Lógica de reflow y ancho máximo de línea.
    """
    def __init__(self, ancho_linea: int = 40):
        self.hijos: List[Linea] = []
        self.ancho_linea = ancho_linea

    def agregar_linea(self, linea: Linea):
        self.hijos.append(linea)

    def contar_palabras(self) -> int:
        return sum(l.contar_palabras() for l in self.hijos)

    def contar_lineas(self) -> int:
        """
        Calcula la cantidad total de líneas generadas.
        AJUSTE CLAVE: Considera la división visual de palabras largas y evita contar
        las líneas que solo contienen la palabra vacía del cursor.
        """
        conteo_lineas = 0
        ancho = self.ancho_linea
        
        # Bandera para saber si el párrafo tiene contenido real (no solo el cursor)
        tiene_contenido_real = any(p.texto.strip() for linea in self.hijos for p in linea.hijos)
        
        for linea in self.hijos:
            # Palabras con texto significativo en esta línea
            palabras_con_texto = [p.texto.strip() for p in linea.hijos if p.texto.strip()]
            
            # Caso especial: Si el párrafo está esencialmente vacío, la línea del cursor cuenta 1.
            if not tiene_contenido_real:
                return 1 if self.hijos else 0

            # Caso 1: La línea solo contiene la palabra vacía del cursor (y hay más contenido en el párrafo)
            if not palabras_con_texto:
                continue # Ignoramos esta línea, ya que es solo la línea de trabajo/cursor.

            # Caso 2: Una única palabra que el reflow puso sola porque es demasiado larga (División Visual)
            if len(palabras_con_texto) == 1 and len(palabras_con_texto[0]) > ancho:
                largo_palabra = len(palabras_con_texto[0])
                # Cuenta cuántas líneas visuales ocupa esta palabra
                lineas_visuales = (largo_palabra + ancho - 1) // ancho 
                conteo_lineas += lineas_visuales
                continue
                
            # Caso 3: Línea estándar (reflow ya la manejó)
            conteo_lineas += 1 

        # Si el conteo resultó 0 (solo queda la línea del cursor y se ignoró), lo fijamos a 1
        if conteo_lineas == 0 and self.hijos:
            return 1
            
        return conteo_lineas

    def mostrar(self) -> str:
        # Usamos "".join() porque cada Linea (vía Strategy) ya devuelve el '\n'.
        return "".join(l.mostrar() for l in self.hijos)

    def cambiar_alineacion(self, nueva_alineacion: IStrategyAlineacion):
        for linea in self.hijos:
            linea.cambiar_alineacion(nueva_alineacion)

    def _obtener_todas_las_palabras(self) -> List[Palabra]:
        """Extrae todas las palabras del párrafo en orden."""
        palabras: List[Palabra] = []
        for linea in self.hijos:
            # Incluye solo palabras con texto, o la ÚNICA palabra vacía de una línea (el cursor)
            palabras.extend(p for p in linea.hijos if p.texto or (len(linea.hijos) == 1 and not p.texto))
        return palabras

    def aplicar_reflow(self) -> None:
        """Reorganiza las palabras en líneas respetando el ancho_linea y sin cortar palabras."""
        todas = self._obtener_todas_las_palabras()
        
        # 1. Determinar la alineación actual antes de limpiar las líneas.
        alineacion_previa = AlineacionIzquierda()
        if self.hijos and self.hijos[0].hijos and self.hijos[0].alineacion:
            alineacion_previa = self.hijos[0].alineacion
        
        self.hijos.clear()
        
        # Caso inicial de párrafo vacío
        if not todas:
            linea_vacia = Linea(ancho=self.ancho_linea)
            linea_vacia.cambiar_alineacion(alineacion_previa)
            linea_vacia.agregar_palabra(Palabra(""))
            self.hijos.append(linea_vacia)
            return

        linea_actual = Linea(ancho=self.ancho_linea)
        linea_actual.cambiar_alineacion(alineacion_previa)
        self.hijos.append(linea_actual)
        longitud = 0
        
        for i, palabra in enumerate(todas):
            largo = len(palabra.texto)
            # Solo añade espacio si hay texto previo y la palabra actual no está vacía
            espacio = 1 if longitud > 0 and largo > 0 else 0 
            
            # Manejo de palabras que exceden el ancho de línea (CRÍTICO)
            if largo > self.ancho_linea:
                if longitud > 0:
                    linea_actual = Linea(ancho=self.ancho_linea)
                    linea_actual.cambiar_alineacion(alineacion_previa)
                    self.hijos.append(linea_actual)
                    longitud = 0
                
                # Agrega la palabra entera, la Strategy la dividirá visualmente
                linea_actual.agregar_palabra(palabra)
                longitud = largo
                
                # Forzar nueva línea después del desborde
                linea_actual = Linea(ancho=self.ancho_linea)
                linea_actual.cambiar_alineacion(alineacion_previa)
                self.hijos.append(linea_actual)
                longitud = 0
                continue
            
            # Lógica de Reflow estándar
            if longitud + espacio + largo > self.ancho_linea:
                nueva_linea = Linea(ancho=self.ancho_linea)
                nueva_linea.cambiar_alineacion(linea_actual.alineacion) 
                
                self.hijos.append(nueva_linea)
                linea_actual = nueva_linea
                
                linea_actual.agregar_palabra(palabra)
                longitud = largo
            else:
                linea_actual.agregar_palabra(palabra)
                longitud += espacio + largo

        # Asegurar que la última línea tenga una palabra vacía para el cursor
        if not linea_actual.hijos or (linea_actual.hijos[-1].texto.strip() and len(linea_actual.hijos) < linea_actual.ancho + 1):
             linea_actual.agregar_palabra(Palabra(""))