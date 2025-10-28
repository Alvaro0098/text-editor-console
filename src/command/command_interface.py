# command/command_interface.py
from abc import ABC, abstractmethod

class ICommand(ABC):
    """Interfaz del patrón Command."""
    @abstractmethod
    def ejecutar(self) -> None:
        pass

    @abstractmethod
    def deshacer(self) -> None:
        pass