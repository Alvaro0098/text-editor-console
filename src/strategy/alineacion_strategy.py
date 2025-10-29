from abc import ABC, abstractmethod
from typing import List

class IStrategyAlineacion(ABC):
    @abstractmethod
    def aplicar_alineacion(self, palabras: List[str], ancho: int) -> str:
        pass

# FUNCIÓN AUXILIAR CLAVE: Divide visualmente una palabra si excede el ancho.
def _dividir_palabras_largas(palabras: List[str], ancho: int) -> List[str]:
    """Divide visualmente una palabra si excede el ancho (solo si es la única palabra en la línea)."""
    if len(palabras) == 1 and len(palabras[0]) > ancho:
        palabra = palabras[0]
        # Divide la palabra en fragmentos del tamaño del ancho
        fragmentos = [palabra[i:i + ancho] for i in range(0, len(palabra), ancho)]
        return fragmentos
    return palabras


class AlineacionIzquierda(IStrategyAlineacion):
    def aplicar_alineacion(self, palabras: List[str], ancho: int) -> str:
        palabras_visibles = _dividir_palabras_largas(palabras, ancho)
        
        # Si la palabra fue dividida visualmente, cada fragmento es una nueva línea
        if len(palabras) == 1 and len(palabras_visibles) > 1:
            lineas = [f.ljust(ancho) for f in palabras_visibles]
            return "\n".join(lineas) + "\n"
        
        texto = " ".join(palabras_visibles)
        return texto.ljust(ancho) + "\n" # Garantiza el salto de línea


class AlineacionDerecha(IStrategyAlineacion):
    def aplicar_alineacion(self, palabras: List[str], ancho: int) -> str:
        palabras_visibles = _dividir_palabras_largas(palabras, ancho)
        
        if len(palabras) == 1 and len(palabras_visibles) > 1:
            lineas = [f.rjust(ancho) for f in palabras_visibles]
            return "\n".join(lineas) + "\n"
        
        texto = " ".join(palabras_visibles)
        return texto.rjust(ancho) + "\n"

class AlineacionCentrada(IStrategyAlineacion):
    def aplicar_alineacion(self, palabras: List[str], ancho: int) -> str:
        palabras_visibles = _dividir_palabras_largas(palabras, ancho)
        
        if len(palabras) == 1 and len(palabras_visibles) > 1:
            lineas = [f.center(ancho) for f in palabras_visibles]
            return "\n".join(lineas) + "\n"
        
        texto = " ".join(palabras_visibles)
        return texto.center(ancho) + "\n"

class AlineacionJustificada(IStrategyAlineacion):
    def aplicar_alineacion(self, palabras: List[str], ancho: int) -> str:
        
        if len(palabras) <= 1:
            if not palabras:
                return " " * ancho + "\n"
            
            # Si hay una palabra larga, se divide visualmente usando la alineación izquierda
            palabras_visibles = _dividir_palabras_largas(palabras, ancho)
            if len(palabras_visibles) > 1:
                lineas = [f.ljust(ancho) for f in palabras_visibles]
                return "\n".join(lineas) + "\n"
            
            return palabras[0].ljust(ancho) + "\n"
        
        # Lógica de Justificación para múltiples palabras
        longitud_total = sum(len(p) for p in palabras)
        espacios = ancho - longitud_total
        huecos = len(palabras) - 1
        base, extra = divmod(espacios, huecos)
        linea = palabras[0]
        for i, palabra in enumerate(palabras[1:], 1):
            linea += " " * (base + (1 if i <= extra else 0)) + palabra
        return linea + "\n"