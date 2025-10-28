# src/command/invoker.py
from typing import List
from .command_interface import ICommand

class CommandInvoker:
    """Invoker - Gestiona la ejecución y el historial de comandos."""
    def __init__(self):
        self._historial: List[ICommand] = [] # Historial de comandos ejecutados (para deshacer)
        self._historial_deshacer: List[ICommand] = [] # Historial de comandos deshechos (para rehacer)

    def ejecutar(self, command: ICommand) -> None:
        """Ejecuta el comando y lo añade al historial. Borra el historial de rehacer."""
        command.ejecutar()
        self._historial.append(command)
        # 🚨 Importante: Si se ejecuta un nuevo comando, se limpia el historial de rehacer.
        self._historial_deshacer = [] 

    def deshacer(self) -> None:
        """Deshace el último comando ejecutado (CTRL+Z)."""
        if self._historial:
            command = self._historial.pop()
            command.deshacer()
            self._historial_deshacer.append(command) # Lo mueve al historial de deshacer

    def rehacer(self) -> None: 
        """Rehace el último comando deshecho (CTRL+Y)."""
        if self._historial_deshacer:
            command = self._historial_deshacer.pop()
            command.ejecutar() # Vuelve a ejecutarlo
            self._historial.append(command) # Lo devuelve al historial principal