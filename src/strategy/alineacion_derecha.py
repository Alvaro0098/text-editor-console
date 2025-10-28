from .alineacion_strategy import IStrategyAlineacion

class AlineacionDerecha(IStrategyAlineacion):
    """Estrategia Concreta - Alinea el texto a la derecha."""
    def aplicar_alineacion(self, texto: str, ancho: int) -> str:
        return texto.rjust(ancho)