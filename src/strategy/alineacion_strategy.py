from abc import ABC, abstractmethod

class IStrategyAlineacion(ABC):
    """Estrategia (Strategy) - Define la interfaz para el algoritmo de alineación."""
    @abstractmethod
    def aplicar_alineacion(self, texto: str, ancho: int) -> str:
        pass