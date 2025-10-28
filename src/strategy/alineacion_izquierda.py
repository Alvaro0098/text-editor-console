from .alineacion_strategy import IStrategyAlineacion


class AlineacionIzquierda(IStrategyAlineacion):
    """Estrategia Concreta: Alineación por defecto."""
    def aplicar_alineacion(self, texto: str, ancho: int) -> str:
        # Usa el método ljust para llenar con espacios a la derecha
        return texto.ljust(ancho)