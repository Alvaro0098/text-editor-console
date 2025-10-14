from abc import ABC, abstractmethod

class ComponentMain(ABC):
    @abstractmethod
    def contar_palabras(self):
        """Cuenta el número de palabras en el componente."""
        pass

    @abstractmethod
    def contar_paginas(self):
        """Cuenta el número de páginas en el componente."""
        pass

    @abstractmethod
    def mostrar(self):
        """Muestra la representación textual del componente."""
        pass