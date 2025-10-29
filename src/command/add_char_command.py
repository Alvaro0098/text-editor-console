from .command_interface import ICommand 
from src.composite.linea import Linea
from src.composite.palabra import Palabra

class AgregarCaracterCommand(ICommand):
    def __init__(self, linea: Linea, palabra_idx: int, char_offset: int, char: str):
        self._linea = linea
        self._palabra_idx = palabra_idx
        self._char_offset = char_offset
        self._char = char
        self._palabra_receptora: Palabra = linea.get_palabra(palabra_idx)
        self.cursor_pos_antes: tuple = None
        self.cursor_pos_despues: tuple = None 

    def ejecutar(self) -> None:
        self._palabra_receptora.insertar_caracter(self._char_offset, self._char)

    def deshacer(self) -> None:
        self._palabra_receptora.eliminar_caracter(self._char_offset)