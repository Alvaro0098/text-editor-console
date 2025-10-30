from typing import List
from src.composite.pagina import Pagina # Asegurado para acceder a MAX_LINEAS_POR_PAGINA
from src.composite.component_main import ComponenteDocumento
from src.composite.parrafo import Parrafo
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
        """
        Aplica reflow a todos los párrafos y recalcula la división en páginas.
        Solución robusta que itera línea por línea.
        """
        
        # 1. Consolidar TODOS los párrafos existentes
        todos_los_parrafos: List[Parrafo] = []
        for pagina in self.hijos:
            todos_los_parrafos.extend(pagina.hijos)

        # 2. Aplicar reflow a todos los párrafos existentes
        for parrafo in todos_los_parrafos:
            parrafo.aplicar_reflow()
            
        # 3. Recalcular la división de páginas línea por línea
        paginas_nuevas: List[Pagina] = []
        pagina_actual = Pagina()
        lineas_en_pagina = 0
        

        for parrafo_original in todos_los_parrafos:
            
            # Inicializamos el párrafo recreado y mantenemos la alineación
            parrafo_recreado = Parrafo(ancho_linea=parrafo_original.ancho_linea)
            # 🚨 FIX STABILITY: Necesitamos acceder a la alineación de la primera línea (si existe)
            alineacion_parrafo = parrafo_original.hijos[0].alineacion if parrafo_original.hijos else None
            if alineacion_parrafo:
                 parrafo_recreado.cambiar_alineacion(alineacion_parrafo)
            
            # Recorremos cada línea del párrafo ya formateado
            for linea in parrafo_original.hijos:
                linea_count = 1 
                
                # A) Lógica de Cambio de Página (utiliza la constante MAX_LINEAS_POR_PAGINA de Pagina)
                if lineas_en_pagina + linea_count > Pagina.MAX_LINEAS_POR_PAGINA:
                    # 1. Finalizamos y agregamos el párrafo actual a la página actual.
                    if parrafo_recreado.hijos:
                        pagina_actual.agregar_parrafo(parrafo_recreado)

                    # 2. Finalizamos la página actual e iniciamos una nueva.
                    if pagina_actual.hijos:
                        paginas_nuevas.append(pagina_actual)
                    
                    pagina_actual = Pagina()
                    lineas_en_pagina = 0
                    
                    # 3. Creamos un NUEVO párrafo recreado para la nueva página
                    parrafo_recreado = Parrafo(ancho_linea=parrafo_original.ancho_linea)
                    if alineacion_parrafo:
                         parrafo_recreado.cambiar_alineacion(alineacion_parrafo)


                # B) Agregamos la línea al párrafo recreado
                parrafo_recreado.agregar_linea(linea)
                lineas_en_pagina += linea_count
            
            # C) Una vez que se terminaron las líneas del párrafo original, 
            # agregamos el último segmento de párrafo recreado a la página.
            if parrafo_recreado.hijos and parrafo_recreado not in pagina_actual.hijos:
                pagina_actual.agregar_parrafo(parrafo_recreado)


        # Añadir la última página
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