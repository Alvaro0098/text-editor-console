from abc import ABC, abstractmethod
from typing import List

class IStrategyAlineacion(ABC):
    """
    ROL: Strategy (Interfaz).
    RESPONSABILIDAD: Definir la interfaz común para todos los algoritmos de alineación
                     soportados por el editor (Izquierda, Derecha, Centrada, Justificada).
    ÍTEM DE CAMBIO OCULTO: Permite añadir nuevas estrategias de alineación sin modificar
                          las clases Linea o Parrafo.
    """
    @abstractmethod
    def aplicar_alineacion(self, palabras: List[str], ancho: int) -> str:
        pass

# FUNCIÓN AUXILIAR CLAVE: Divide visualmente una palabra si excede el ancho.
def _dividir_palabras_largas(palabras: List[str], ancho: int) -> List[str]:
    """
    Función auxiliar para dividir una palabra si su longitud excede el ancho de la línea.
    Esto asegura que el reflow y el renderizado no rompan el formato.
    """
    if len(palabras) == 1 and palabras[0] == '\n': # Excluir el ancla de salto de linea
        return ['\n']
        
    if len(palabras) == 1 and len(palabras[0]) > ancho:
        palabra = palabras[0]
        # Divide la palabra en fragmentos del tamaño del ancho
        fragmentos = [palabra[i:i + ancho] for i in range(0, len(palabra), ancho)]
        return fragmentos
    return palabras


class AlineacionIzquierda(IStrategyAlineacion):
    """
    ROL: Concrete Strategy.
    RESPONSABILIDAD: Implementar el algoritmo de alineación a la izquierda,
                     añadiendo espacios a la derecha del texto para alcanzar el ancho.
    ÍTEM DE CAMBIO OCULTO: La implementación específica de ljust (alineación izquierda).
    """
    def aplicar_alineacion(self, palabras: List[str], ancho: int) -> str:
        palabras_visibles = _dividir_palabras_largas(palabras, ancho)
        
        # Si la palabra fue dividida visualmente, cada fragmento es una nueva línea
        if len(palabras) == 1 and len(palabras_visibles) > 1:
            lineas = [f.ljust(ancho) for f in palabras_visibles]
            return "\n".join(lineas) + "\n"
        
        texto = " ".join(palabras_visibles)
        return texto.ljust(ancho) + "\n" # Garantiza el salto de línea


class AlineacionDerecha(IStrategyAlineacion):
    """
    ROL: Concrete Strategy.
    RESPONSABILIDAD: Implementar el algoritmo de alineación a la derecha,
                     añadiendo espacios a la izquierda del texto para alcanzar el ancho.
    ÍTEM DE CAMBIO OCULTO: La implementación específica de rjust (alineación derecha).
    """
    def aplicar_alineacion(self, palabras: List[str], ancho: int) -> str:
        palabras_visibles = _dividir_palabras_largas(palabras, ancho)
        
        if len(palabras) == 1 and len(palabras_visibles) > 1:
            lineas = [f.rjust(ancho) for f in palabras_visibles]
            return "\n".join(lineas) + "\n"
        
        texto = " ".join(palabras_visibles)
        return texto.rjust(ancho) + "\n"

class AlineacionCentrada(IStrategyAlineacion):
    """
    ROL: Concrete Strategy.
    RESPONSABILIDAD: Implementar el algoritmo de alineación centrada,
                     distribuyendo equitativamente los espacios a ambos lados del texto.
    ÍTEM DE CAMBIO OCULTO: La implementación específica de center (alineación centrada).
    """
    def aplicar_alineacion(self, palabras: List[str], ancho: int) -> str:
        palabras_visibles = _dividir_palabras_largas(palabras, ancho)
        
        if len(palabras) == 1 and len(palabras_visibles) > 1:
            lineas = [f.center(ancho) for f in palabras_visibles]
            return "\n".join(lineas) + "\n"
        
        texto = " ".join(palabras_visibles)
        return texto.center(ancho) + "\n"

class AlineacionJustificada(IStrategyAlineacion):
    """
    ROL: Concrete Strategy.
    RESPONSABILIDAD: Implementar el algoritmo de alineación justificada, distribuyendo
                     los espacios vacíos entre las palabras para que la línea ocupe
                     exactamente el ancho definido.
    ÍTEM DE CAMBIO OCULTO: La lógica matemática para distribuir los espacios remanentes
                          (uso de divmod).
    """
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
        
        # divmod(a, b) retorna (a // b, a % b) -> (base, extra)
        base, extra = divmod(espacios, huecos)
        
        linea = palabras[0]
        # Se itera sobre las palabras desde la segunda (índice 1) hasta el final
        for i, palabra in enumerate(palabras[1:], 1):
            # Agrega la cantidad base de espacios + 1 extra para los primeros 'extra' huecos
            num_espacios = base + (1 if i <= extra else 0)
            linea += " " * num_espacios + palabra
            
        return linea + "\n"