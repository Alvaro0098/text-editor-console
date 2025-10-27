# composite/parrafo.py
class Parrafo(ComponenteDocumento):
    """Compuesto (Composite) - Contiene líneas y gestiona el 'reflow' de palabras."""
    def __init__(self):
        self.hijos: List[Linea] = []

    def agregar_linea(self, linea: Linea):
        self.hijos.append(linea)

    def contar_palabras(self) -> int:
        return sum(hijo.contar_palabras() for hijo in self.hijos)

    def mostrar(self) -> str:
        """Responsabilidad: Unir las líneas, añadiendo un salto de línea entre ellas."""
        return "\n".join(hijo.mostrar() for hijo in self.hijos)
    
    # Este método gestionaría el 'reflow' (ajuste de líneas por ancho fijo)
    # Se debe implementar para que las palabras no se corten. (Requisito clave)
    def aplicar_reflow(self, ancho_linea: int):
        # Lógica de reajuste de palabras en líneas. 
        # (Ítem de Cambio Escondido: Cómo se maneja el ancho fijo y el corte de palabras).
        pass