from typing import List

class CommandInvoker:
    """Invocador/Gestor Deshacer - Almacena comandos para permitir el Undo."""
    def __init__(self):
        self.historial: List[ICommand] = []

    def ejecutar(self, command: ICommand) -> None:
        """Responsabilidad: Ejecuta un comando y lo guarda en el historial."""
        command.ejecutar()
        self.historial.append(command)

    def deshacer(self) -> None:
        """Responsabilidad: Deshace la última operación (CTRL+Z)."""
        if self.historial:
            comando = self.historial.pop()
            comando.deshacer()