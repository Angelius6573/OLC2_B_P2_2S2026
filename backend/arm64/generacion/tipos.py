"""Lectura de los textos de tipo que deja el checker y su traducción a celdas y manejadores.

El checker escribe los tipos como texto: 'i32', 'String', '[i32; 3]', '[[i32; 3]; 2]'. Un
'[T; n]' tiene la dimensión exterior desconocida en compilación (split, repetidor con cantidad
variable). Un arreglo es un bloque plano en row-major: sus celdas se cuentan
multiplicando los tamaños de todas sus dimensiones.
"""
from backend.arm64.errores import ErrorGeneracion

MANEJADORES = {
    'i32': 'ox_print_i32',
    'f64': 'ox_print_f64',
    'bool': 'ox_print_bool',
    'char': 'ox_print_char',
    'String': 'ox_print_string',
}
MANEJADORES_DEPURACION = {
    **MANEJADORES,
    'char': 'ox_print_char_debug',
    'String': 'ox_print_string_debug',
}

def es_arreglo(tipo):
    return isinstance(tipo, str) and tipo.startswith('[')

def es_par(tipo):
    # String y arreglo ocupan las dos palabras del slot: puntero en +0 y longitud en +8
    return tipo == 'String' or es_arreglo(tipo)

def elemento(tipo):
    return tipo[1:tipo.rindex(';')].strip()

def longitud(tipo):
    texto = tipo[tipo.rindex(';') + 1:-1].strip()
    return int(texto) if texto.isdigit() else None

def celdas(tipo, nodo=None):
    """Celdas de 16 bytes que ocupa un valor de este tipo dentro de un bloque plano."""
    if not es_arreglo(tipo):
        return 1
    n = longitud(tipo)
    if n is None:
        raise ErrorGeneracion(
            f"El arreglo '{tipo}' tiene una dimensión interior sin tamaño constante; "
            'en row-major cada dimensión interior debe conocerse en compilación',
            *posicion(nodo))
    return n * celdas(elemento(tipo), nodo)

def manejador(tipo, depuracion):
    if es_arreglo(tipo):
        return 'ox_print_array'
    tabla = MANEJADORES_DEPURACION if depuracion else MANEJADORES
    if tipo not in tabla:
        raise ErrorGeneracion(f"No se puede imprimir un valor de tipo '{tipo}'")
    return tabla[tipo]

def descriptor(tipo):
    """Entradas .quad del descriptor de ox_print_array para un arreglo de este tipo."""
    elem = elemento(tipo)
    if es_arreglo(elem):
        return ['ox_print_array', str(celdas(elem)), str(longitud(elem)), *descriptor(elem)]
    return [manejador(elem, depuracion=True), '0', '0']

def nombre_descriptor(tipo):
    # El descriptor solo depende del elemento: [i32; 3] y [i32; 5] comparten descriptor_i32
    elem = elemento(tipo)
    nombre = elem.replace('[', 'arreglo_').replace(']', '').replace(';', '').replace(' ', '_')
    return f'descriptor_{nombre.lower()}'

def posicion(nodo):
    if nodo is None:
        return 0, 0
    return getattr(nodo, 'linea', 0) or 0, getattr(nodo, 'columna', 0) or 0
