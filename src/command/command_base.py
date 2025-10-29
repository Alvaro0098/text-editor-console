# src/command/command_base.py
from abc import ABC, abstractmethod

class CommandBase(ABC):
    """Interfaz base para los comandos del patrón Command."""

    @abstractmethod
    def ejecutar(self) -> None:
        pass

    @abstractmethod
    def deshacer(self) -> None:
        pass
