class AlineacionJustificada(IStrategyAlineacion):
    """Estrategia Concreta - Alinea el texto a la derecha y a la izquierda (Justificado)."""
    def aplicar_alineacion(self, texto: str, ancho: int) -> str:
        # Ítem de Cambio Escondido: Lógica compleja de distribuir espacios entre palabras.
        # IMPLEMENTAR: Distribuir uniformemente los espacios para ocupar 'ancho'.
        # Por ahora, un retorno simple:
        return texto.center(ancho) # Placeholder, necesita lógica de justificación real.