from typing import List
from src.composite.parrafo import Parrafo
from src.composite.component_main import ComponenteDocumento

class Pagina(ComponenteDocumento):
    """
    Contenedor de párrafos. Gestiona la división del contenido si excede el límite.
    Patrón de Diseño: Composite (Component).
    Ítem de Cambio Oculto: Límite físico de contenido (MAX_LINEAS_POR_PAGINA).
    """
    # 🚨 FIX CRUCIAL: Límite de 8 líneas.
    MAX_LINEAS_POR_PAGINA = 8

    def __init__(self):
        self.hijos: List[Parrafo] = []

    def agregar_parrafo(self, parrafo: Parrafo):
        self.hijos.append(parrafo)

    def dividir_en_paginas(self) -> List["Pagina"]:
        """
        Divide el contenido en páginas. Nota: La lógica principal de paginación
        se centraliza en Documento.actualizar_paginas(). Este método se usa
        principalmente para compatibilidad o para dividir una página individual.
        """
        paginas: List[Pagina] = []
        pagina_actual = Pagina()
        lineas_en_pagina = 0
        
        for parrafo in self.hijos:
            parrafo.aplicar_reflow() # Asegura que esté en formato
            
            # Lógica de división simplificada (usa el párrafo completo como unidad de división)
            parrafo_lineas = parrafo.contar_lineas()
            
            if lineas_en_pagina + parrafo_lineas > Pagina.MAX_LINEAS_POR_PAGINA and lineas_en_pagina > 0:
                paginas.append(pagina_actual)
                pagina_actual = Pagina()
                lineas_en_pagina = 0
            
            pagina_actual.agregar_parrafo(parrafo)
            lineas_en_pagina += parrafo_lineas

        if pagina_actual.hijos:
            paginas.append(pagina_actual)
            
        return paginas

    def contar_palabras(self) -> int:
        return sum(p.contar_palabras() for p in self.hijos)

    def contar_lineas(self) -> int:
        return sum(p.contar_lineas() for p in self.hijos)

    def mostrar(self) -> str:
        return "\n\n".join(p.mostrar() for p in self.hijos)