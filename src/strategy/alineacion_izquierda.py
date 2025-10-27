class AlineacionIzquierda(IStrategyAlineacion):
    """Estrategia Concreta - Alinea el texto a la izquierda."""
    def aplicar_alineacion(self, texto: str, ancho: int) -> str:
        return texto.ljust(ancho)