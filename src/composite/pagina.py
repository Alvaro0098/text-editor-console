# composite/pagina.py
class Pagina(ComponenteDocumento):
    """Compuesto (Composite) - Contiene párrafos."""
    def __init__(self):
        self.hijos: List[Parrafo] = []

    def agregar_parrafo(self, parrafo: Parrafo):
        self.hijos.append(parrafo)

    def contar_palabras(self) -> int:
        return sum(hijo.contar_palabras() for hijo in self.hijos)

    def mostrar(self) -> str:
        """Responsabilidad: Unir los párrafos, añadiendo un salto entre ellos."""
        return "\n\n".join(hijo.mostrar() for hijo in self.hijos)