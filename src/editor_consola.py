# editor/editor_consola.py
from composite.documento import Documento
from composite.pagina import Pagina, Parrafo, Linea, Palabra
from command.invoker import CommandInvoker
from command.agregar_caracter_command import AgregarCaracterCommand
from command.eliminar_caracter_command import EliminarCaracterCommand
from strategy.alineacion_strategy import IStrategyAlineacion
# Importar todas las estrategias concretas

class EditorConsola:
    """Controlador - Orquesta las acciones del usuario, el CommandInvoker y el Documento."""
    def __init__(self, ancho_linea: int = 80):
        self.documento = Documento()
        self.ancho_linea = ancho_linea
        self.invoker = CommandInvoker()
        
        # Inicialización de estructura mínima
        linea = Linea(ancho=ancho_linea)
        parrafo = Parrafo()
        parrafo.agregar_linea(linea)
        pagina = Pagina()
        pagina.agregar_parrafo(parrafo)
        self.documento.agregar_pagina(pagina)
        
        # Cursor simplificado (se asume que siempre está en la primera línea)
        self.cursor = (0, 0, 0, 0, 0) # p_idx, par_idx, lin_idx, palabra_idx, char_offset

    def current_linea(self) -> Linea:
        """Eficiencia: Acceso rápido a la línea actual del cursor."""
        p_idx, par_idx, lin_idx, _, _ = self.cursor
        return self.documento.hijos[p_idx].hijos[par_idx].hijos[lin_idx]
    
    # --- API de Operaciones (Creación de Comandos) ---

    def insertar_caracter(self, caracter: str) -> None:
        """Genera y ejecuta el comando de inserción, moviendo el cursor."""
        _, _, _, palabra_idx, char_offset = self.cursor
        linea = self.current_linea()
        cmd = AgregarCaracterCommand(linea, palabra_idx, char_offset, caracter)
        self.invoker.ejecutar(cmd)
        
        # Mover cursor (Responsabilidad del Controlador)
        self.cursor = (self.cursor[0], self.cursor[1], self.cursor[2], palabra_idx, char_offset + 1)
        # La lógica de reflow debería llamarse aquí: self.current_parrafo().aplicar_reflow(self.ancho_linea)

    def eliminar_caracter(self) -> None:
        """Genera y ejecuta el comando de eliminación, moviendo el cursor."""
        _, _, _, palabra_idx, char_offset = self.cursor
        if char_offset == 0: return # No borrar si está al inicio

        borrar_pos = char_offset - 1
        linea = self.current_linea()
        cmd = EliminarCaracterCommand(linea, palabra_idx, borrar_pos)
        self.invoker.ejecutar(cmd)
        
        # Mover cursor
        self.cursor = (self.cursor[0], self.cursor[1], self.cursor[2], palabra_idx, borrar_pos)

    def deshacer(self) -> None:
        """Cumple requisito de CTRL+Z."""
        self.invoker.deshacer()
        
    def cambiar_alineacion(self, nueva_estrategia: IStrategyAlineacion) -> None:
        """Usa el Contexto (Linea) para cambiar la Estrategia (Alineacion)."""
        linea = self.current_linea()
        # Esto debería ser un Command para que sea reversible
        linea.cambiar_alineacion(nueva_estrategia) 

    # --- API de Estadísticas y Vista ---
    
    def mostrar_documento(self) -> None:
        """Muestra el contenido del documento formateado."""
        print("=== Vista Reducida (Ancho Fijo) ===")
        print(self.documento.mostrar())
        print("====================================")

    def mostrar_estadisticas(self) -> None:
        """Muestra las estadísticas del documento."""
        palabras = self.documento.contar_palabras()
        paginas = self.documento.contar_paginas()
        print(f"Estadísticas: {palabras} palabras, {paginas} páginas.")