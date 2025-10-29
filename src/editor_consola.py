from src.composite.documento import Documento
from src.composite.pagina import Pagina
from src.composite.parrafo import Parrafo
from src.composite.linea import Linea
from src.composite.palabra import Palabra
from src.command.invoke import CommandInvoker
from src.command.add_char_command import AgregarCaracterCommand
from src.command.delete_char_command import EliminarCaracterCommand
from src.strategy.alineacion_strategy import (
    IStrategyAlineacion,
    AlineacionIzquierda,
    AlineacionDerecha,
    AlineacionCentrada,
    AlineacionJustificada
)
from typing import Tuple

class EditorConsola:
    """
    Controlador central del editor. Maneja cursor, invoker de comandos, documento y estado de alineación.
    Patrón de Diseño: Fachada (Facade) / Command (Cliente).
    Ítem de Cambio Oculto: Flujo de interacción de comandos y lógica de cursor.
    """

    def __init__(self, ancho_linea: int = 40):
        self.documento = Documento()
        self.ancho_linea = ancho_linea
        self.invoker = CommandInvoker()

        # Inicialización de la estructura mínima (Pagina -> Parrafo -> Linea -> Palabra)
        linea = Linea(ancho=ancho_linea)
        linea.agregar_palabra(Palabra("")) 
        parrafo = Parrafo(ancho_linea=ancho_linea)
        parrafo.agregar_linea(linea)
        pagina = Pagina()
        pagina.agregar_parrafo(parrafo)
        self.documento.agregar_pagina(pagina)

        # Cursor: (p_idx, par_idx, lin_idx, palabra_idx, char_offset)
        self.cursor: Tuple[int, int, int, int, int] = (0, 0, 0, 0, 0) 
        self.alineacion_actual: IStrategyAlineacion = AlineacionIzquierda() 
        self.current_parrafo().cambiar_alineacion(self.alineacion_actual)
        self.documento.actualizar_paginas() 

    def current_linea(self) -> Linea:
        p_idx, par_idx, lin_idx, _, _ = self.cursor
        return self.documento.hijos[p_idx].hijos[par_idx].hijos[lin_idx]

    def current_parrafo(self) -> Parrafo:
        p_idx, par_idx, _, _, _ = self.cursor
        return self.documento.hijos[p_idx].hijos[par_idx]

    def current_palabra(self) -> Palabra:
        _, _, _, palabra_idx, _ = self.cursor
        return self.current_linea().get_palabra(palabra_idx)

    def current_pagina(self) -> Pagina:
        p_idx, _, _, _, _ = self.cursor
        return self.documento.hijos[p_idx]

    def set_cursor(self, palabra_idx: int, char_offset: int) -> None:
        p_idx, par_idx, lin_idx, _, _ = self.cursor
        self.cursor = (p_idx, par_idx, lin_idx, palabra_idx, char_offset)
        
    def ensure_word_exists(self, palabra_idx: int):
        """
        Asegura que la palabra en la posición del cursor exista,
        usando la lógica de get_palabra de Linea.
        """
        linea = self.current_linea()
        linea.get_palabra(palabra_idx)


    def _recalcular_cursor_post_reflow(self, palabra_ref: Palabra, offset: int):
        """Encuentra la nueva posición del cursor después de un reflow, usando la referencia al objeto Palabra."""
        p_idx, par_idx, _, _, _ = self.cursor
        parrafo = self.current_parrafo()
        
        # Iterar el nuevo árbol de líneas para encontrar la palabra por referencia
        for lin_idx, linea in enumerate(parrafo.hijos):
            for w_idx, palabra in enumerate(linea.hijos):
                if palabra is palabra_ref:
                    self.cursor = (p_idx, par_idx, lin_idx, w_idx, offset)
                    return
        
        # Si no se encuentra (caso raro, como borrar todo), resetea
        self.cursor = (p_idx, par_idx, 0, 0, 0)

    def insertar_caracter(self, caracter: str):
        cursor_ant = self.cursor
        _, _, _, palabra_idx, char_offset = self.cursor
        linea = self.current_linea()
        palabra_mod = self.current_palabra()

        cmd = AgregarCaracterCommand(linea, palabra_idx, char_offset, caracter)
        cmd.cursor_pos_antes = cursor_ant

        self.invoker.ejecutar(cmd)
        
        nuevo_offset = char_offset + 1
        
        # Aplicar reflow en el párrafo actual y recalcular la paginación global
        self.current_parrafo().aplicar_reflow()
        self.documento.actualizar_paginas() 
        
        # Recalcular la posición del cursor
        self._recalcular_cursor_post_reflow(palabra_mod, nuevo_offset)
        cmd.cursor_pos_despues = self.cursor

    def eliminar_caracter(self):
        cursor_ant = self.cursor
        _, _, _, palabra_idx, char_offset = self.cursor
        if char_offset == 0:
            return
        
        borrar_pos = char_offset - 1
        linea = self.current_linea()
        palabra_mod = self.current_palabra()

        cmd = EliminarCaracterCommand(linea, palabra_idx, borrar_pos)
        cmd.cursor_pos_antes = cursor_ant

        self.invoker.ejecutar(cmd)
        
        # Aplicar reflow en el párrafo actual y recalcular la paginación global
        self.current_parrafo().aplicar_reflow()
        self.documento.actualizar_paginas() 
        
        self._recalcular_cursor_post_reflow(palabra_mod, borrar_pos)
        cmd.cursor_pos_despues = self.cursor

    def deshacer(self):
        cmd = self.invoker.deshacer()
        if cmd and hasattr(cmd, 'cursor_pos_antes'):
            self.current_parrafo().aplicar_reflow()
            self.documento.actualizar_paginas()
            self.cursor = cmd.cursor_pos_antes

    def rehacer(self):
        cmd = self.invoker.rehacer()
        if cmd and hasattr(cmd, 'cursor_pos_despues'):
            self.current_parrafo().aplicar_reflow()
            self.documento.actualizar_paginas()
            self.cursor = cmd.cursor_pos_despues

    def cambiar_alineacion(self, nombre: str):
        estrategias = {
            "izquierda": AlineacionIzquierda(),
            "derecha": AlineacionDerecha(),
            "centrada": AlineacionCentrada(),
            "justificada": AlineacionJustificada()
        }
        est = estrategias.get(nombre.lower())
        if est:
            self.alineacion_actual = est
            self.current_parrafo().cambiar_alineacion(est)
            # Reaplicar reflow para que la alineación justificada se muestre bien
            self.current_parrafo().aplicar_reflow() 
            self.documento.actualizar_paginas()


    def mostrar_documento(self):
        # Asegurarse de que el documento esté correctamente paginado antes de mostrar estadísticas
        self.documento.actualizar_paginas() 
        
        parrafos = self.documento.contar_parrafos()
        palabras = self.documento.contar_palabras()
        paginas = self.documento.contar_paginas()
        lineas = self.documento.contar_lineas()
        
        print("=" * self.ancho_linea)
        print(f"📊 Palabras: {palabras} | Párrafos: {parrafos} | Líneas: {lineas} | Páginas: {paginas}")
        print(f"📌 Cursor: {self.cursor} | Alineación: {self.alineacion_actual.__class__.__name__}")
        print("=" * self.ancho_linea)
        print(self.documento.mostrar())
        print("=" * self.ancho_linea)
        print() # <--- ¡Corrección de visualización: Salto de línea forzado!

        