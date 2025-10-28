# command/eliminar_caracter_command.py
from .command_interface import ICommand 
from src.composite.linea import Linea

from src.composite.palabra import Palabra
class EliminarCaracterCommand(ICommand):
    def __init__(self, linea: Linea, palabra_idx: int, char_pos: int):
        self._linea = linea
        self._palabra_idx = palabra_idx
        self._char_pos = char_pos # Posición del caracter a borrar
        self._caracter_borrado = ""
        self._palabra_receptora = linea.get_palabra(palabra_idx)

    def ejecutar(self) -> None:
        # Guardar el caracter que se borra para poder deshacer
        self._caracter_borrado = self._palabra_receptora.eliminar_caracter(self._char_pos)

    def deshacer(self) -> None:
        # Deshacer implica reinsertar el caracter borrado en la posición original
        self._palabra_receptora.insertar_caracter(self._char_pos, self._caracter_borrado)