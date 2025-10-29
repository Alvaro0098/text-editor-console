from abc import ABC, abstractmethod
from typing import List


class IStrategyAlineacion(ABC):
    """Interfaz para el patrón Strategy (alineación de texto)."""
    @abstractmethod
    def aplicar_alineacion(self, palabras: List[str], ancho: int) -> str:
        """
        Toma una lista de palabras que componen la línea y el ancho total.
        Devuelve la cadena de texto con la alineación aplicada.
        """
        pass

# 2. ESTRATEGIAS CONCRETAS
class AlineacionIzquierda(IStrategyAlineacion):
    """Estrategia Concreta: Alineación por defecto (izquierda)."""
    def aplicar_alineacion(self, palabras: List[str], ancho: int) -> str:
        texto = " ".join(palabras)
        return texto.ljust(ancho)


class AlineacionDerecha(IStrategyAlineacion):
    """Estrategia Concreta - Alinea el texto a la derecha."""
    def aplicar_alineacion(self, palabras: List[str], ancho: int) -> str:
        texto = " ".join(palabras)
        return texto.rjust(ancho)


class AlineacionCentrada(IStrategyAlineacion): 
    """Estrategia Concreta - Alinea el texto al centro."""
    def aplicar_alineacion(self, palabras: List[str], ancho: int) -> str:
        texto = " ".join(palabras)
        return texto.center(ancho)


class AlineacionJustificada(IStrategyAlineacion):
    """Estrategia Concreta - Alinea el texto a la derecha y a la izquierda (Justificado)."""
    def aplicar_alineacion(self, palabras: List[str], ancho: int) -> str:
        texto_base = " ".join(palabras)
        
      
        if len(palabras) <= 1:
            return texto_base.ljust(ancho)

        longitud_actual = len("".join(palabras))
        espacios_totales = ancho - longitud_actual
        num_huecos = len(palabras) - 1
        
        espacios_base = espacios_totales // num_huecos
        espacios_extra = espacios_totales % num_huecos
        
        linea_final = palabras[0]
        for i in range(1, len(palabras)):
            espacios = espacios_base + (1 if i <= espacios_extra else 0)
            linea_final += " " * espacios + palabras[i]
            
        return linea_final.ljust(ancho)