# composite/linea.py
from strategy.alineacion_strategy import IStrategyAlineacion
from strategy.alineacion_izquierda import AlineacionIzquierda

class Linea(ComponenteDocumento):
    """Compuesto (Composite) - Contiene palabras y aplica una estrategia de alineación."""
    def __init__(self, ancho: int = 80, alineacion: IStrategyAlineacion = AlineacionIzquierda()):
        self.hijos: List[Palabra] = []
        self.ancho: int = ancho
        # Contexto del patrón Strategy
        self.alineacion: IStrategyAlineacion = alineacion

    def agregar_palabra(self, palabra: Palabra) -> None:
        self.hijos.append(palabra)

    def contar_palabras(self) -> int:
        """Responsabilidad: Delega el conteo a sus palabras."""
        return sum(hijo.contar_palabras() for hijo in self.hijos)

    def mostrar(self) -> str:
        """Responsabilidad: Aplica la alineación a su contenido (Usa Strategy)."""
        texto = " ".join(hijo.mostrar() for hijo in self.hijos)
        return self.alineacion.aplicar_alineacion(texto, self.ancho)
    
    def cambiar_alineacion(self, nueva_alineacion: IStrategyAlineacion) -> None:
        """Ítem de Cambio Escondido: El algoritmo de alineación."""
        self.alineacion = nueva_alineacion
        
    # Métodos de edición simplificados para uso por Command
    def get_palabra(self, idx: int) -> Palabra:
        return self.hijos[idx]