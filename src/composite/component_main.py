from abc import ABC, abstractmethod

class ComponenteDocumento(ABC):
    """
    Componente - Define la interfaz común para todos los elementos estructurales.
    Patrón de Diseño: Composite (Component).
    Ítem de Cambio Oculto: La estructura y las operaciones comunes (mostrar, contar).
    """
    @abstractmethod
    def contar_palabras(self) -> int:
        """Cuenta el número de palabras en el componente."""
        pass
    
    @abstractmethod
    def contar_lineas(self) -> int:
        """Cuenta el número de líneas en el componente."""
        pass

    @abstractmethod
    def mostrar(self) -> str:
        """Muestra la representación formateada del componente."""
        pass