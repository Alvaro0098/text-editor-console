import os
import sys
import time
import keyboard 
from typing import List
from .editor_consola import EditorConsola

from .strategy.alineacion_strategy import (
    AlineacionIzquierda, 
    AlineacionCentrada, 
    AlineacionDerecha, 
    AlineacionJustificada,
    IStrategyAlineacion
)

ANCHO_CONSOLA: int = 80
EDITOR_GLOBAL: EditorConsola = EditorConsola(ancho_linea=ANCHO_CONSOLA)

def limpiar_consola() -> None:
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def dibujar_hoja() -> None:
    limpiar_consola()
    
    estrategia = EDITOR_GLOBAL.alineacion_actual
    
    print("="*ANCHO_CONSOLA)
    print(" " * ((ANCHO_CONSOLA-30)//2) + "PROCESADOR DE TEXTO CONSOLA")
    print("="*ANCHO_CONSOLA)
    print(" COMANDOS RÁPIDOS: Ctrl+Z (Retroceder) | Ctrl+Y (Rehacer) | Ctrl+L (Formato) | Ctrl+S (Cerrar)")
    print("="*ANCHO_CONSOLA)
    
    nombre_estrategia = estrategia.__class__.__name__ 
    if nombre_estrategia.startswith("Alineacion"):
        nombre_estrategia = nombre_estrategia[10:]
        
    print(f" Alineación actual: {nombre_estrategia.upper()}")
    print("="*ANCHO_CONSOLA)
    
    EDITOR_GLOBAL.mostrar_documento()
    
    print("\n" + "="*ANCHO_CONSOLA)
    print("Comience a usar el editor cuando quiera...")

def manejar_tecla(event) -> None:
    
    if event.event_type != keyboard.KEY_DOWN:
        return

    
    if event.name == 'z' and keyboard.is_pressed('ctrl'):
        EDITOR_GLOBAL.deshacer()
        dibujar_hoja()
        return

    if event.name == 'y' and keyboard.is_pressed('ctrl'):
        EDITOR_GLOBAL.rehacer()
        dibujar_hoja()
        return
        
    if event.name == 's' and keyboard.is_pressed('ctrl'):
        print("\nGracias por usar nuestro editor. Vuelva pronto")
        
        keyboard.unhook_all()
        
        sys.stdout.flush()
        
        os._exit(0)
        
    
    if event.name == 'l' and keyboard.is_pressed('ctrl'):
        alineaciones = [AlineacionIzquierda(), AlineacionCentrada(), AlineacionDerecha(), AlineacionJustificada()]
        estrategia_actual = EDITOR_GLOBAL.alineacion_actual
        
        estrategia_actual_index = next((i for i, a in enumerate(alineaciones) if type(a).__name__ == type(estrategia_actual).__name__), 0)
        nueva_estrategia_nombre = alineaciones[(estrategia_actual_index + 1) % len(alineaciones)].__class__.__name__[10:].lower()

        EDITOR_GLOBAL.cambiar_alineacion(nueva_estrategia_nombre)
        dibujar_hoja()
        return

    
    if len(event.name) == 1 or event.name in ['space', 'enter']:
        char = event.name
        
        if char == 'enter':
            char = '\n' 
        elif char == 'space':
            char = ' '
        
        EDITOR_GLOBAL.insertar_caracter(char)
        dibujar_hoja()
        return

    
    elif event.name == 'backspace':
        EDITOR_GLOBAL.eliminar_caracter()
        dibujar_hoja()
        return

def main_live_editor():
    
    EDITOR_GLOBAL.ensure_word_exists(0) 
    dibujar_hoja() 
    
    keyboard.hook(manejar_tecla)
    
    try:
        while True:
            time.sleep(0.1) 
    except KeyboardInterrupt:
        print("\nSaliendo por interrupción (Ctrl+C).")
        keyboard.unhook_all()
        sys.exit(0)


if __name__ == '__main__':
    main_live_editor()