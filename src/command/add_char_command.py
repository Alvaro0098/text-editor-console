# 4. src/command/agregar_caracter_command.py (CORREGIDO)
from .command_interface import ICommand # <--- ¡Añadido! (relativo)
# CORRECCIÓN DE RUTA: Busca los receptores en el paquete 'composite'
from src.composite.linea import Linea
from src.composite.palabra import Palabra
class AgregarCaracterCommand(ICommand):
    def __init__(self, linea: Linea, palabra_idx: int, char_offset: int, char: str):
        self._linea = linea
        self._palabra_idx = palabra_idx
        self._char_offset = char_offset
        self._char = char
        self._palabra_receptora: Palabra = linea.get_palabra(palabra_idx)

    def ejecutar(self) -> None:
        self._palabra_receptora.insertar_caracter(self._char_offset, self._char)

    def deshacer(self) -> None:
        # Deshacer implica eliminar el caracter que se agregó
        self._palabra_receptora.eliminar_caracter(self._char_offset)