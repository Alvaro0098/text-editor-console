from .component_main import ComponenteDocumento
from typing import TYPE_CHECKING, Any

# Evita dependencias circulares usando TYPE_CHECKING
if TYPE_CHECKING:
    from .linea import Linea

class Palabra(ComponenteDocumento):
    """
    Representa una palabra en el documento. Es el elemento terminal o Hoja.
    Patrón de Diseño: Composite (Leaf).
    Ítem de Cambio Oculto: La representación mínima de texto y su longitud.
    """

    def __init__(self, texto: str = "", parent: 'Linea' | None = None):
        self.texto = texto
        self.parent = parent # Referencia al padre (Linea)

    def insertar_caracter(self, index: int, char: str):
        """Inserta un caracter en la posición index."""
        if index < 0 or index > len(self.texto):
            index = len(self.texto)
        self.texto = self.texto[:index] + char + self.texto[index:]

    def eliminar_caracter(self, index: int):
        """Elimina un caracter en la posición index."""
        if 0 <= index < len(self.texto):
            self.texto = self.texto[:index] + self.texto[index+1:]

    def contar_palabras(self) -> int:
        """Cada palabra cuenta como 1 si no está vacía."""
        return 1 if self.texto.strip() else 0

    def contar_lineas(self) -> int:
        """Una palabra no cuenta como línea por sí misma."""
        return 0

    def mostrar(self) -> str:
        return self.texto

    def longitud(self) -> int:
        return len(self.texto)