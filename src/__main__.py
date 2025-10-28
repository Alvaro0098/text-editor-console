# main.py (Reemplazar todo el contenido)

import os
import sys
import time
import keyboard # 🚨 Requiere: pip install keyboard
from typing import List

# Importar el controlador de nuestro paquete
from .editor_consola import EditorConsola
# Importar las estrategias necesarias para el ciclo de alineación
from .strategy.alineacion_strategy import (
    AlineacionIzquierda, 
    AlineacionCentrada, 
    AlineacionDerecha, 
    AlineacionJustificada,
    IStrategyAlineacion
)

# --- Variables Globales (Singleton del Editor) ---
ANCHO_CONSOLA: int = 80
EDITOR_GLOBAL: EditorConsola = EditorConsola(ancho_linea=ANCHO_CONSOLA)
# Nota: La clase EditorConsola ya maneja el Invoker (historial), el Documento y el Cursor.
# Ya no necesitamos variables globales para CURSOR_POS, HISTORIAL o DOCUMENTO_ACTUAL.

# --- Funciones de Utilidad (Limpieza y Dibujo) ---

def limpiar_consola() -> None:
    """Borra la pantalla para simular la hoja en blanco."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def dibujar_hoja() -> None:
    """Limpia la pantalla y dibuja el contenido actual del documento usando el Editor global."""
    limpiar_consola()
    
    doc = EDITOR_GLOBAL.documento
    estrategia = EDITOR_GLOBAL.alineacion_actual
    
    print("="*ANCHO_CONSOLA)
    print(" " * ((ANCHO_CONSOLA-30)//2) + "EDITOR DE TEXTO EN VIVO")
    print("="*ANCHO_CONSOLA)
    print(" COMANDOS: Ctrl+Z (Deshacer) | Ctrl+Y (Rehacer) | Ctrl+L (Alinear) | Ctrl+S (Salir)")
    print("="*ANCHO_CONSOLA)
    print(f" Alineación actual: {estrategia.__class__.__name__[10:].upper()}")
    print("="*ANCHO_CONSOLA)
    
    # Dibujamos el contenido de la hoja
    # Usamos mostrar_documento, que usa doc.mostrar()
    EDITOR_GLOBAL.mostrar_documento()
    
    # Simulación de la línea de comandos/cursor
    print("\n" + "="*ANCHO_CONSOLA)
    print("ESPERANDO TECLA...") 
    
# --- Lógica de Manejo de Comandos (Patrón Command y Strategy) ---

def manejar_tecla(event) -> None:
    """Función hook que se llama con cada pulsación de teclado."""
    
    # Solo procesamos eventos de tecla presionada (KEY_DOWN)
    if event.event_type != keyboard.KEY_DOWN:
        return

    # 1. COMANDOS RESERVADOS (Ctrl+Z, Ctrl+Y, Ctrl+S)
    
    if event.name == 'z' and keyboard.is_pressed('ctrl'):
        EDITOR_GLOBAL.deshacer()
        # Se necesita aplicar el reflow/reestructuración aquí si está implementado
        dibujar_hoja()
        return

    if event.name == 'y' and keyboard.is_pressed('ctrl'):
        EDITOR_GLOBAL.rehacer()
        dibujar_hoja()
        return
        
    if event.name == 's' and keyboard.is_pressed('ctrl'):
        print("\nSaliendo del editor. Gracias por usar los patrones de diseño.")
        keyboard.unhook_all()
        sys.exit(0)
        
    # 2. COMANDOS DE ALINEACIÓN (Ctrl+L - Patrón Strategy)
    if event.name == 'l' and keyboard.is_pressed('ctrl'):
        alineaciones = [AlineacionIzquierda(), AlineacionCentrada(), AlineacionDerecha(), AlineacionJustificada()]
        estrategia_actual = EDITOR_GLOBAL.alineacion_actual
        
        # Lógica para ciclar la estrategia
        estrategia_actual_index = next((i for i, a in enumerate(alineaciones) if type(a).__name__ == type(estrategia_actual).__name__), 0)
        nueva_estrategia_nombre = alineaciones[(estrategia_actual_index + 1) % len(alineaciones)].__class__.__name__[10:].lower()

        EDITOR_GLOBAL.cambiar_alineacion(nueva_estrategia_nombre)
        dibujar_hoja()
        return

    # 3. EDICIÓN EN VIVO (Caracteres Normales)

    # Tecla de Espacio, Enter, o un caracter simple que no es una tecla de control.
    if len(event.name) == 1 or event.name in ['space', 'enter']:
        char = event.name
        
        if char == 'enter':
            # Nota: Esto inserta un salto de línea/nueva palabra. 
            # La lógica de párrafo debe ser manejada en EditorConsola o Reflow.
            char = '\n' 
        elif char == 'space':
            char = ' '
        
        # Ejecutar el comando de agregar (Patrón Command)
        EDITOR_GLOBAL.insertar_caracter(char)
        dibujar_hoja()
        return

    # 4. TECLA BACKSPACE
    elif event.name == 'backspace':
        # Ejecutar el comando de borrar (Patrón Command)
        EDITOR_GLOBAL.eliminar_caracter()
        dibujar_hoja()
        return

# --- Función Principal ---

def main_live_editor():
    """Punto de entrada: Inicializa el editor en modo de escucha de teclado."""
    
    # Aseguramos la existencia de una palabra inicial para el cursor
    EDITOR_GLOBAL.ensure_word_exists(0) 
    
    dibujar_hoja() 
    
    # Iniciar la escucha de teclado
    keyboard.hook(manejar_tecla)
    
    # Esperar el comando de salida (Ctrl+S)
    try:
        # Usa un ciclo infinito si el 'wait' no funciona
        keyboard.wait('ctrl+s') 
    except KeyboardInterrupt:
        pass
    
    keyboard.unhook_all()
    sys.exit(0)

if __name__ == '__main__':
    main_live_editor()