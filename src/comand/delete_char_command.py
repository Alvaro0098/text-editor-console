class EliminarCaracterCommand(ICommand):
    """Comando Concreto - Elimina un carácter en una línea/palabra."""
    def __init__(self, linea: Linea, palabra_idx: int, char_offset: int):
        self.linea = linea
        self.palabra_idx = palabra_idx
        self.char_offset = char_offset
        self.eliminado = "" # Se guarda el estado para el deshacer

    def ejecutar(self) -> None:
        """Receptor: La línea modifica la palabra y guarda el carácter eliminado."""
        palabra = self.linea.get_palabra(self.palabra_idx)
        self.eliminado = palabra.eliminar_caracter(self.char_offset)

    def deshacer(self) -> None:
        """Reversa la operación insertando el carácter guardado."""
        if self.eliminado:
            palabra = self.linea.get_palabra(self.palabra_idx)
            # Reinsertar el caracter en la misma posición que fue borrado
            palabra.insertar_caracter(self.char_offset, self.eliminado)