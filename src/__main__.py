import os
import sys
import time
import keyboard 
from typing import List
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
    
    # Obtiene el estado actual
    estrategia = EDITOR_GLOBAL.alineacion_actual
    
    print("="*ANCHO_CONSOLA)
    print(" " * ((ANCHO_CONSOLA-30)//2) + "PROCESADOR DE TEXTO CONSOLA")
    print("="*ANCHO_CONSOLA)
    print(" COMANDOS RÁPIDOS: Ctrl+Z (Retroceder) | Ctrl+Y (Rehacer) | Ctrl+L (Formato) | Ctrl+S (Cerrar)")
    print("="*ANCHO_CONSOLA)
    
    # Obtiene el nombre de la estrategia para mostrarlo
    nombre_estrategia = estrategia.__class__.__name__ 
    if nombre_estrategia.startswith("Alineacion"):
        nombre_estrategia = nombre_estrategia[10:]
        
    print(f" Alineación actual: {nombre_estrategia.upper()}")
    print("="*ANCHO_CONSOLA)
    
    # Dibuja el contenido
    EDITOR_GLOBAL.mostrar_documento()
    
    print("\n" + "="*ANCHO_CONSOLA)
    print("Comience a usar el editor cuando quiera...")

# --- Lógica de Manejo de Comandos (Patrón Command y Strategy) ---

def manejar_tecla(event) -> None:
    """Función hook que se llama con cada pulsación de teclado."""
    
    if event.event_type != keyboard.KEY_DOWN:
        return

    # 1. COMANDOS RESERVADOS (Ctrl+Z, Ctrl+Y, Ctrl+S)
    
    if event.name == 'z' and keyboard.is_pressed('ctrl'):
        EDITOR_GLOBAL.deshacer()
        dibujar_hoja()
        return

    if event.name == 'y' and keyboard.is_pressed('ctrl'):
        EDITOR_GLOBAL.rehacer()
        dibujar_hoja()
        return
        
    if event.name == 's' and keyboard.is_pressed('ctrl'):
        # 🚨 SOLUCIÓN PIPÍ CUCÚ PARA SALIDA LIMPIA (os._exit)
        print("\nGracias por usar nuestro editor. Vuelva pronto")
        
        # 1. Desactivar el hook y liberar el thread de keyboard
        keyboard.unhook_all()
        
        # 2. Forzar la escritura de cualquier buffer de salida pendiente
        sys.stdout.flush()
        
        # 3. Salida inmediata del proceso, evitando el conflicto de threads al finalizar
        os._exit(0)
        
    # 2. COMANDOS DE ALINEACIÓN (Ctrl+L - Patrón Strategy)
    if event.name == 'l' and keyboard.is_pressed('ctrl'):
        alineaciones = [AlineacionIzquierda(), AlineacionCentrada(), AlineacionDerecha(), AlineacionJustificada()]
        estrategia_actual = EDITOR_GLOBAL.alineacion_actual
        
        estrategia_actual_index = next((i for i, a in enumerate(alineaciones) if type(a).__name__ == type(estrategia_actual).__name__), 0)
        nueva_estrategia_nombre = alineaciones[(estrategia_actual_index + 1) % len(alineaciones)].__class__.__name__[10:].lower()

        EDITOR_GLOBAL.cambiar_alineacion(nueva_estrategia_nombre)
        dibujar_hoja()
        return

    # 3. EDICIÓN EN VIVO (Caracteres Normales)
    if len(event.name) == 1 or event.name in ['space', 'enter']:
        char = event.name
        
        if char == 'enter':
            char = '\n' 
        elif char == 'space':
            char = ' '
        
        EDITOR_GLOBAL.insertar_caracter(char)
        dibujar_hoja()
        return

    # 4. TECLA BACKSPACE
    elif event.name == 'backspace':
        EDITOR_GLOBAL.eliminar_caracter()
        dibujar_hoja()
        return

# --- Función Principal ---

def main_live_editor():
    """Punto de entrada: Inicializa el editor en modo de escucha de teclado."""
    
    EDITOR_GLOBAL.ensure_word_exists(0) 
    dibujar_hoja() 
    
    keyboard.hook(manejar_tecla)
    
    # Esperamos indefinidamente por el evento Ctrl+S
    try:
        # Bucle de espera simple para mantener el hilo principal vivo
        while True:
            time.sleep(0.1) 
    except KeyboardInterrupt:
        # Este manejo es para el caso de que alguien use Ctrl+C, aunque Ctrl+S ya usa os._exit(0)
        print("\nSaliendo por interrupción (Ctrl+C).")
        keyboard.unhook_all()
        sys.exit(0)


if __name__ == '__main__':
    main_live_editor()