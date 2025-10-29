from typing import List
from src.composite.pagina import Pagina
from src.composite.component_main import ComponenteDocumento
# NUEVA IMPORTACIÓN REQUERIDA
from src.composite.parrafo import Parrafo 
# IMPORTACIÓN REQUERIDA SI SE MANIPULAN LINEAS DIRECTAMENTE EN EL DOCUMENTO
from src.composite.linea import Linea 

class Documento(ComponenteDocumento):
    """
    Raíz del documento. Contenedor principal de Paginas.
    Patrón de Diseño: Composite (Root/Component).
    Ítem de Cambio Oculto: Lógica de paginación global y estadísticas totales.
    """
    def __init__(self):
        self.hijos: List[Pagina] = []

    def agregar_pagina(self, pagina: Pagina):
        self.hijos.append(pagina)

    def actualizar_paginas(self):
        """Aplica reflow a todos los párrafos y recalcula la división en páginas."""
        paginas_nuevas: List[Pagina] = []
        
        # 1. Aplicar reflow a todos los párrafos existentes
        for pagina in self.hijos:
            for parrafo in pagina.hijos:
                parrafo.aplicar_reflow()
        
        # 2. Recalcular la división de páginas basada en los párrafos con reflow
        # Esto es más complejo: debemos consolidar todos los párrafos antes de dividir.
        
        todos_los_parrafos: List[Parrafo] = []
        for pagina in self.hijos:
            todos_los_parrafos.extend(pagina.hijos)
            
        pagina_actual = Pagina()
        lineas_en_pagina = 0
        
        for parrafo in todos_los_parrafos:
            # CORRECCIÓN: Ahora 'Parrafo' está definido por la importación
            parrafo_dividido = Parrafo(ancho_linea=parrafo.ancho_linea)
            
            for linea in parrafo.hijos:
                linea_count = 1
                
                if lineas_en_pagina + linea_count > Pagina.MAX_LINEAS_POR_PAGINA and lineas_en_pagina > 0:
                    # La línea no cabe, cerramos la página actual y la añadimos
                    paginas_nuevas.append(pagina_actual)
                    pagina_actual = Pagina()
                    lineas_en_pagina = 0
                    parrafo_dividido = Parrafo(ancho_linea=parrafo.ancho_linea)
                
                # Agrega la línea al párrafo dividido temporal
                parrafo_dividido.agregar_linea(linea)
                lineas_en_pagina += linea_count

            # Agrega el párrafo (posiblemente dividido) a la página actual
            if parrafo_dividido.hijos:
                pagina_actual.hijos.append(parrafo_dividido)

        if pagina_actual.hijos:
            paginas_nuevas.append(pagina_actual)
            
        self.hijos = paginas_nuevas


    def contar_palabras(self) -> int:
        return sum(p.contar_palabras() for p in self.hijos)

    def contar_lineas(self) -> int:
        return sum(p.contar_lineas() for p in self.hijos)

    def contar_paginas(self) -> int:
        return len(self.hijos)

    def contar_parrafos(self) -> int:
        return sum(len(pagina.hijos) for pagina in self.hijos)

    def mostrar(self) -> str:
        separador = "=" * 40
        salida = []
        for i, pagina in enumerate(self.hijos, start=1):
            salida.append(f"{separador}\n📄 Página {i}\n{separador}\n{pagina.mostrar()}")
        return "\n\n".join(salida)