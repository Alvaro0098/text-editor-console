from typing import List
from src.composite.palabra import Palabra
from src.composite.component_main import ComponenteDocumento
from src.strategy.alineacion_strategy import IStrategyAlineacion, AlineacionIzquierda

class Linea(ComponenteDocumento):
    """
    Contenedor de palabras. Aplica la estrategia de alineación para la vista.
    Patrón de Diseño: Composite (Component) / Strategy (Context).
    Ítem de Cambio Oculto: Lógica de formato y ancho fijo (a través de Strategy).
    """
    def __init__(self, ancho: int = 40):
        self.hijos: List[Palabra] = []
        self.ancho = ancho
        self.alineacion: IStrategyAlineacion = AlineacionIzquierda()

    def agregar_palabra(self, palabra: Palabra):
        """Agrega una palabra a la línea y establece la referencia al padre."""
        palabra.parent = self # Establece la referencia al padre
        self.hijos.append(palabra)

    def get_palabra(self, index: int) -> Palabra:
        """Asegura que exista la palabra en el índice (rellenando con vacías si es necesario)."""
        while len(self.hijos) <= index:
            # Al crear Palabra vacía, asignarle el padre (self)
            self.hijos.append(Palabra("", parent=self)) 
        return self.hijos[index]

    def contar_palabras(self) -> int:
        return sum(p.contar_palabras() for p in self.hijos)
    
    def contar_lineas(self) -> int:
        """Una línea cuenta como 1."""
        return 1

    def cambiar_alineacion(self, nueva_alineacion: IStrategyAlineacion):
        self.alineacion = nueva_alineacion

    def mostrar(self) -> str:
        palabras_texto = [p.texto for p in self.hijos if p.texto]
        return self.alineacion.aplicar_alineacion(palabras_texto, self.ancho)