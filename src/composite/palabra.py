from dataclasses import dataclass
from .component_main import ComponenteDocumento

@dataclass
class Palabra(ComponenteDocumento):
    """Hoja (Leaf) - Representa la unidad mínima de texto."""
    texto: str

    def contar_palabras(self) -> int:
        """Responsabilidad: Cuenta una palabra si no está vacía."""
        return 1 if self.texto.strip() else 0

    def mostrar(self) -> str:
        """Responsabilidad: Retorna su propio texto."""
        return self.texto
    
    def insertar_caracter(self, index: int, char: str) -> None:
        if index <= 0: self.texto = char + self.texto
        elif index >= len(self.texto): self.texto = self.texto + char
        else: self.texto = self.texto[:index] + char + self.texto[index:]

    def eliminar_caracter(self, index: int) -> str:
        if 0 <= index < len(self.texto):
            removed = self.texto[index]
            self.texto = self.texto[:index] + self.texto[index+1:]
            return removed
        return ""