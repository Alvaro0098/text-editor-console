# src/editor_consola.py

from .composite.documento import Documento
from .composite.pagina import Pagina
from .composite.parrafo import Parrafo
from .composite.linea import Linea
from .composite.palabra import Palabra

# Asume que aquí importas tu CommandInvoker y Commands
from .command.invoke import CommandInvoker
from .command.add_char_command import AgregarCaracterCommand
from .command.delete_char_command import EliminarCaracterCommand

# Importación de estrategias
from .strategy.alineacion_strategy import (
    IStrategyAlineacion, 
    AlineacionIzquierda, 
    AlineacionDerecha, 
    AlineacionCentrada, 
    AlineacionJustificada
)

# ------------------------------------------------------------------
class EditorConsola:
    """
    Controlador - Orquesta las acciones del usuario, el CommandInvoker y el Documento.
    Responsabilidad: Gestionar el cursor y la creación/ejecución de comandos.
    """
    def __init__(self, ancho_linea: int = 80):
        self.documento = Documento()
        self.ancho_linea = ancho_linea
        self.invoker = CommandInvoker() # Asumimos que CommandInvoker tiene rehacer.
        
        # Inicialización de estructura mínima
        linea = Linea(ancho=ancho_linea)
        linea.hijos.append(Palabra("")) 
        parrafo = Parrafo()
        parrafo.agregar_linea(linea)
        pagina = Pagina()
        pagina.agregar_parrafo(parrafo)
        self.documento.agregar_pagina(pagina)
        
        self.cursor = (0, 0, 0, 0, 0) 
        
        # Para controlar la alineación actual del último párrafo
        self.alineacion_actual = AlineacionIzquierda() 
        # Esta llamada ahora funcionará porque Parrafo tiene cambiar_alineacion:
        self.current_parrafo().cambiar_alineacion(self.alineacion_actual) 

    def current_linea(self) -> Linea:
        p_idx, par_idx, lin_idx, _, _ = self.cursor
        return self.documento.hijos[p_idx].hijos[par_idx].hijos[lin_idx]
    
    def current_parrafo(self) -> Parrafo:
        p_idx, par_idx, _, _, _ = self.cursor
        return self.documento.hijos[p_idx].hijos[par_idx]

    def ensure_word_exists(self, word_idx: int):
        linea = self.current_linea()
        if not linea.hijos or word_idx >= len(linea.hijos):
            linea.hijos.append(Palabra(texto=""))

    def set_cursor(self, palabra_idx: int, char_offset: int) -> None:
        p_idx, par_idx, lin_idx, _, _ = self.cursor
        self.cursor = (p_idx, par_idx, lin_idx, palabra_idx, char_offset)
    
    # --- API de Operaciones (Creación de Comandos) ---

    def insertar_caracter(self, caracter: str) -> None:
        _, _, _, palabra_idx, char_offset = self.cursor
        linea = self.current_linea()
        
        cmd = AgregarCaracterCommand(linea, palabra_idx, char_offset, caracter)
        self.invoker.ejecutar(cmd)
        
        self.set_cursor(palabra_idx, char_offset + 1)
        
        # self.current_parrafo().aplicar_reflow(self.ancho_linea) # <-- PENDIENTE CRÍTICO

    def eliminar_caracter(self) -> None:
        _, _, _, palabra_idx, char_offset = self.cursor
        if char_offset == 0: return 

        borrar_pos = char_offset - 1
        linea = self.current_linea()
        cmd = EliminarCaracterCommand(linea, palabra_idx, borrar_pos)
        self.invoker.ejecutar(cmd)
        
        self.set_cursor(palabra_idx, borrar_pos)

    def deshacer(self) -> None:
        self.invoker.deshacer()
        
    def rehacer(self) -> None: 
        self.invoker.rehacer()
        
    def cambiar_alineacion(self, nombre_estrategia: str) -> None: 
        estrategias = {
            "izquierda": AlineacionIzquierda(),
            "derecha": AlineacionDerecha(),
            "centrada": AlineacionCentrada(),
            "justificada": AlineacionJustificada()
        }
        
        estrategia = estrategias.get(nombre_estrategia.lower())
        
        if estrategia:
            self.alineacion_actual = estrategia
            parrafo = self.current_parrafo()
            parrafo.cambiar_alineacion(estrategia)
            print(f"Alineación cambiada a: {nombre_estrategia.upper()}")
        else:
            print(f"Estrategia de alineación '{nombre_estrategia}' no reconocida. Opciones: izquierda, derecha, centrada, justificada.")

    # --- API de Estadísticas y Vista ---
    
    def mostrar_documento(self) -> None:
        print("=" * self.ancho_linea)
        print(f"=== Vista Reducida (Ancho Fijo: {self.ancho_linea}) ===")
        print(f"Cursor en: P: {self.cursor[0]}, Par: {self.cursor[1]}, Lin: {self.cursor[2]}, W: {self.cursor[3]}, Ch: {self.cursor[4]}")
        print("=" * self.ancho_linea)
        print(self.documento.mostrar())
        print("=" * self.ancho_linea)

    def mostrar_estadisticas(self) -> None:
        palabras = self.documento.contar_palabras()
        paginas = self.documento.contar_paginas()
        print(f"Estadísticas: {palabras} palabras, {paginas} páginas.")