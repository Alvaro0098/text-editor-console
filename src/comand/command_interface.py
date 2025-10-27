from abc import ABC, abstractmethod

class ICommand(ABC):
    """Comando (Command) - Interfaz para todas las operaciones ejecutables y reversibles."""
    @abstractmethod
    def ejecutar(self) -> None:
        pass

    @abstractmethod
    def deshacer(self) -> None:
        pass