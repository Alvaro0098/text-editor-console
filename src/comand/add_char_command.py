from composite.linea import Linea

class AgregarCaracterCommand(ICommand):
    """Comando Concreto - Inserta un carácter en una línea/palabra."""
    def __init__(self, linea: Linea, palabra_idx: int, char_offset: int, caracter: str):
        self.linea = linea
        self.palabra_idx = palabra_idx
        self.char_offset = char_offset
        self.caracter = caracter

    def ejecutar(self) -> None:
        """Receptor: La línea modifica la palabra."""
        palabra = self.linea.get_palabra(self.palabra_idx)
        palabra.insertar_caracter(self.char_offset, self.caracter)
        # Nota: La lógica de Reflow debería ejecutarse después de la inserción.

    def deshacer(self) -> None:
        """Reversa la operación eliminando el carácter."""
        palabra = self.linea.get_palabra(self.palabra_idx)
        palabra.eliminar_caracter(self.char_offset)