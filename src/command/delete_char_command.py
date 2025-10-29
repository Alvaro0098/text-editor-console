from ..composite.linea import Linea
from ..composite.palabra import Palabra
from .command_base import CommandBase

class EliminarCaracterCommand(CommandBase):
    """Comando para eliminar un carácter de una palabra específica."""

    def __init__(self, linea: Linea, palabra_idx: int, char_idx: int):
        self.linea = linea
        self.palabra_idx = palabra_idx
        self.char_idx = char_idx
        self.cursor_pos_antes = None
        self.cursor_pos_despues = None

        # Se accede a la palabra mediante get_palabra() para compatibilidad
        self._palabra_receptora: Palabra = linea.get_palabra(palabra_idx)
        self._caracter_eliminado = ""

    def ejecutar(self):
        texto = self._palabra_receptora.texto
        if self.char_idx < len(texto):
            self._caracter_eliminado = texto[self.char_idx]
            self._palabra_receptora.texto = texto[:self.char_idx] + texto[self.char_idx+1:]

    def deshacer(self):
        texto = self._palabra_receptora.texto
        # Reinsertamos el carácter eliminado
        self._palabra_receptora.texto = texto[:self.char_idx] + self._caracter_eliminado + texto[self.char_idx:]
