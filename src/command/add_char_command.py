from ..composite.linea import Linea
from ..composite.palabra import Palabra
from src.command.command_base import CommandBase


class AgregarCaracterCommand(CommandBase):
    """Comando para agregar un carácter en una palabra específica."""
    
    def __init__(self, linea: Linea, palabra_idx: int, char_idx: int, caracter: str):
        self.linea = linea
        self.palabra_idx = palabra_idx
        self.char_idx = char_idx
        self.caracter = caracter
        self.cursor_pos_antes = None
        self.cursor_pos_despues = None

        # Se accede a la palabra mediante get_palabra() para compatibilidad
        self._palabra_receptora: Palabra = linea.get_palabra(palabra_idx)

    def ejecutar(self):
        texto = self._palabra_receptora.texto
        # Insertamos el carácter en la posición indicada
        self._palabra_receptora.texto = texto[:self.char_idx] + self.caracter + texto[self.char_idx:]

    def deshacer(self):
        texto = self._palabra_receptora.texto
        # Eliminamos el carácter insertado
        self._palabra_receptora.texto = texto[:self.char_idx] + texto[self.char_idx+1:]
