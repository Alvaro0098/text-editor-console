# src/main.py
from editor.editor_consola import EditorConsola

def repl():
    editor = EditorConsola(ancho_linea=40)
    editor.ensure_word_exists(0)

    print("Editor simple (comandos): insert <char> | del | undo | show | setcursor <word_idx> <char_offset> | exit")
    while True:
        line = input("> ").strip()
        if not line:
            continue
        parts = line.split()
        cmd = parts[0].lower()

        if cmd == "exit":
            break
        elif cmd == "show":
            editor.mostrar_documento()
        elif cmd == "insert":
            if len(parts) >= 2:
                ch = " ".join(parts[1:])  # allow inserting space as 'insert  '
                # por simplicidad, permitimos insertar strings (se usaría por caracter)
                for c in ch:
                    editor.insertar_caracter(c)
            else:
                print("Uso: insert <caracter(es)>")
        elif cmd == "del":
            editor.eliminar_caracter()
        elif cmd == "undo":
            editor.deshacer()
        elif cmd == "setcursor":
            if len(parts) == 3:
                try:
                    wi = int(parts[1])
                    co = int(parts[2])
                    editor.set_cursor(wi, co)
                except ValueError:
                    print("Indices invalidos")
            else:
                print("Uso: setcursor <word_idx> <char_offset>")
        else:
            print("Comando desconocido")

if __name__ == "__main__":
    repl()
