errores = []

def reportar(categoria, linea, columna, mensaje):
    errores.append((linea, columna, f"[{categoria}] {mensaje}"))

def limpiar():
    errores.clear()
