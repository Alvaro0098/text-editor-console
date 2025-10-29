class AlineacionJustificada(IStrategyAlineacion):
    """Estrategia Concreta - Alinea el texto a la derecha y a la izquierda (Justificado)."""
    def aplicar_alineacion(self, texto: str, ancho: int) -> str:
    
        return texto.center(ancho) 