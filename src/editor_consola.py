from .composite.documento import Documento
from .composite.pagina import Pagina
from .composite.parrafo import Parrafo
from .composite.linea import Linea
from .composite.palabra import Palabra
from typing import List 
from .command.invoke import CommandInvoker
from .command.add_char_command import AgregarCaracterCommand
from .command.delete_char_command import EliminarCaracterCommand
from .strategy.alineacion_strategy import (
    IStrategyAlineacion, 
    AlineacionIzquierda, 
    AlineacionDerecha, 
    AlineacionCentrada, 
    AlineacionJustificada
)

ANSI_CURSOR = "\033[7m \033[0m"  

class EditorConsola:
    """
    Controlador - Orquesta las acciones del usuario, el CommandInvoker y el Documento.
    Responsabilidad: Gestionar el cursor y la creación/ejecución de comandos.
    """
    def __init__(self, ancho_linea: int = 80):
        self.documento = Documento()
        self.ancho_linea = ancho_linea
        self.invoker = CommandInvoker() 

        linea = Linea(ancho=ancho_linea)
        linea.hijos.append(Palabra("")) 
        parrafo = Parrafo()
        parrafo.agregar_linea(linea)
        pagina = Pagina()
        pagina.agregar_parrafo(parrafo)
        self.documento.agregar_pagina(pagina)
        self.cursor = (0, 0, 0, 0, 0) 
        self.alineacion_actual = AlineacionIzquierda() 
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
    
    def _recalcular_cursor_post_reflow(self, palabra_referencia: Palabra, offset_caracter: int):
        """Busca las nuevas coordenadas de línea/palabra para el cursor después del reflow."""
        
        p_idx, par_idx, _, _, _ = self.cursor 
        parrafo = self.current_parrafo()
        
        for nueva_lin_idx, linea in enumerate(parrafo.hijos):
            for nueva_w_idx, palabra in enumerate(linea.hijos):
                if palabra is palabra_referencia:
                    self.cursor = (p_idx, par_idx, nueva_lin_idx, nueva_w_idx, offset_caracter)
                    return

        self.cursor = (p_idx, par_idx, 0, 0, 0)


    def insertar_caracter(self, caracter: str) -> None:
    
        cursor_pos_anterior = self.cursor 
        _, _, _, palabra_idx, char_offset = self.cursor
        linea = self.current_linea()
        palabra_modificada = linea.hijos[palabra_idx] 
        
        cmd = AgregarCaracterCommand(linea, palabra_idx, char_offset, caracter)
        cmd.cursor_pos_antes = cursor_pos_anterior
        
        self.invoker.ejecutar(cmd)
        
        nuevo_offset = char_offset + 1
        self.current_parrafo().aplicar_reflow(self.ancho_linea) 
        self._recalcular_cursor_post_reflow(palabra_modificada, nuevo_offset)


        cmd.cursor_pos_despues = self.cursor 

    def eliminar_caracter(self) -> None:

        cursor_pos_anterior = self.cursor 

        _, _, _, palabra_idx, char_offset = self.cursor
        if char_offset == 0: return 

        borrar_pos = char_offset - 1
        linea = self.current_linea()
        palabra_modificada = linea.hijos[palabra_idx] 
        
        cmd = EliminarCaracterCommand(linea, palabra_idx, borrar_pos)
        cmd.cursor_pos_antes = cursor_pos_anterior 
        
        self.invoker.ejecutar(cmd)
        
        self.current_parrafo().aplicar_reflow(self.ancho_linea) 
        
        self._recalcular_cursor_post_reflow(palabra_modificada, borrar_pos)

        cmd.cursor_pos_despues = self.cursor 

# src/editor_consola.py (SOLO MODIFICACIONES EN DESHACER/REHACER)

    def deshacer(self) -> None:
        comando_deshecho = self.invoker.deshacer()
        
        if comando_deshecho and hasattr(comando_deshecho, 'cursor_pos_antes'):
            
            # 1. 🚩 ESTABILIZAR EL DOCUMENTO: Aplicar Reflow al texto recién deshecho.
            #    Esto garantiza que las palabras estén en las líneas correctas antes de posicionar.
            self.current_parrafo().aplicar_reflow(self.ancho_linea)
            
            # 2. RESTAURAR EL CURSOR: Usar la posición que era válida en el estado anterior.
            self.cursor = comando_deshecho.cursor_pos_antes
            
    def rehacer(self) -> None: 
        comando_rehecho = self.invoker.rehacer()
        
        if comando_rehecho and hasattr(comando_rehecho, 'cursor_pos_despues'):
            
            # 1. ESTABILIZAR EL DOCUMENTO: Aplicar Reflow al texto recién rehecho.
            self.current_parrafo().aplicar_reflow(self.ancho_linea)
            
            # 2. RESTAURAR EL CURSOR: Usar la posición que fue calculada después de la acción original.
            self.cursor = comando_rehecho.cursor_pos_despues
        
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

    
    def _get_documento_renderizado_con_cursor(self) -> str:
        """Renderiza el documento y luego inyecta el cursor en el string final."""
        
        doc_texto = self.documento.mostrar()
        
        if not doc_texto:
            return ANSI_CURSOR
            
        lineas = doc_texto.split('\n')
        
        c_p_idx, c_par_idx, c_lin_idx, c_w_idx, c_ch_offset = self.cursor
        
        linea_idx_absoluta = c_lin_idx 
        
        if linea_idx_absoluta >= len(lineas):
            return doc_texto

        linea_a_modificar = lineas[linea_idx_absoluta]
        
        cursor_pos_absoluta = 0
        linea_modelo = self.current_linea()
        
        for i, palabra_obj in enumerate(linea_modelo.hijos):
            palabra_str = palabra_obj.texto
            
            if i == c_w_idx:
                pos_inyeccion = cursor_pos_absoluta + c_ch_offset
                
                if pos_inyeccion < len(linea_a_modificar):
                    char_a_reemplazar = linea_a_modificar[pos_inyeccion]
                    char_con_cursor = f"\033[7m{char_a_reemplazar}\033[0m"
                    
                    linea_modificada = (linea_a_modificar[:pos_inyeccion] + 
                                        char_con_cursor + 
                                        linea_a_modificar[pos_inyeccion + 1:])
                    
                else:
                    texto_sin_relleno = linea_a_modificar.rstrip()
                    espacios_necesarios = pos_inyeccion - len(texto_sin_relleno)
                    
                    linea_modificada = texto_sin_relleno + " " * espacios_necesarios + ANSI_CURSOR
                    
                    linea_modificada = linea_modificada.ljust(self.ancho_linea + len(ANSI_CURSOR) - 2)
                    
                lineas[linea_idx_absoluta] = linea_modificada
                break 

            cursor_pos_absoluta += len(palabra_str)
            if i < len(linea_modelo.hijos) - 1:
                cursor_pos_absoluta += 1 
        
        return "\n".join(lineas)

    def mostrar_documento(self) -> None:
        print("=" * self.ancho_linea)
        print(f"=== Vista Reducida (Ancho Fijo: {self.ancho_linea}) ===")
        print(f"Cursor en: P: {self.cursor[0]}, Par: {self.cursor[1]}, Lin: {self.cursor[2]}, W: {self.cursor[3]}, Ch: {self.cursor[4]}")
        print("=" * self.ancho_linea)
        
        print(self._get_documento_renderizado_con_cursor())
        
        print("=" * self.ancho_linea)

    def mostrar_estadisticas(self) -> None:
        palabras = self.documento.contar_palabras()
        paginas = self.documento.contar_paginas()
        print(f"Estadísticas: {palabras} palabras, {paginas} páginas.")