from typing import List
from .command_interface import ICommand

class CommandInvoker:
    """Invoker - Gestiona la ejecución y el historial de comandos."""
    def __init__(self):
        self._historial: List[ICommand] = []
        self._historial_deshacer: List[ICommand] = [] 

    def ejecutar(self, command: ICommand) -> None:
        """Ejecuta el comando y lo añade al historial. Borra el historial de rehacer."""
        command.ejecutar()
        self._historial.append(command)
        self._historial_deshacer = [] 

    def deshacer(self) -> ICommand | None:
        """Deshace el último comando ejecutado (CTRL+Z) y lo retorna."""
        if self._historial:
            command = self._historial.pop()
            command.deshacer()
            self._historial_deshacer.append(command)
            return command
        return None

    def rehacer(self) -> ICommand | None: 
        """Rehace el último comando deshecho (CTRL+Y) y lo retorna."""
        if self._historial_deshacer: 
            command = self._historial_deshacer.pop()
            command.ejecutar()
            self._historial.append(command)
            return command
        return None