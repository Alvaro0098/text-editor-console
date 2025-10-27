# composite/component_main.py
from abc import ABC, abstractmethod
from typing import List, Union

class ComponenteDocumento(ABC):
    """Componente - Define la interfaz común para la estructura del documento."""
    @abstractmethod
    def contar_palabras(self) -> int:
        """Cuenta el número de palabras en el componente."""
        pass
    
    @abstractmethod
    def mostrar(self) -> str:
        """Muestra la representación formateada del componente."""
        pass