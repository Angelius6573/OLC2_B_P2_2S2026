from backend.ast_modular.aritmetica import Variable
from backend.ast_modular.arrays import AccederIndice
from backend.checker.tipos import LITERALES, NUMERICOS, TIPOS_PRIMITIVOS

def es_literal(nodo):
    return isinstance(nodo, LITERALES)

def se_esperaba(analizador, nodo, esperado, obtenido):
    analizador.error(nodo.linea, nodo.columna, f"Se esperaba '{esperado}', pero se obtuvo '{obtenido}'")

def verificar_asignacion(analizador, nodo, tipo, tipo_valor):
    if tipo == tipo_valor:
        return
    if es_literal(nodo.valor):
        analizador.error(nodo.linea, nodo.columna, f"No se puede asignar un literal de tipo '{tipo_valor}' a una variable de tipo '{tipo}'")
    else:
        se_esperaba(analizador, nodo, tipo, tipo_valor)

def verificar_tipo_definido(analizador, tipo, nodo):
    if tipo in TIPOS_PRIMITIVOS or tipo.startswith('[') or tipo.startswith('&'):
        return
    if analizador.tabla.buscar_struct(tipo) is not None:
        return
    analizador.error(nodo.linea, nodo.columna, f"El tipo '{tipo}' no está definido")

def tipo_elemento(tipo_array):
    if tipo_array.startswith('[') and ';' in tipo_array:
        return tipo_array[1:tipo_array.rindex(';')].strip()
    return None

def tamano_arreglo(tipo_array):
    if not (tipo_array.startswith('[') and ';' in tipo_array and tipo_array.endswith(']')):
        return None
    try:
        return int(tipo_array[tipo_array.rindex(';') + 1:-1].strip())
    except ValueError:
        return None

def nombre_objetivo(nodo):
    if isinstance(nodo, Variable):
        return nodo.id
    if isinstance(nodo, AccederIndice):
        return nombre_objetivo(nodo.objetivo)
    return 'arreglo'

def binaria(op, izquierda, derecha):
    if op == '+':
        if izquierda == 'String' and derecha == 'String':
            return 'String'
        if izquierda in NUMERICOS and derecha in NUMERICOS:
            return 'f64' if izquierda != derecha else izquierda
        return None
    if op == '-':
        if izquierda in NUMERICOS and derecha in NUMERICOS:
            return 'f64' if izquierda != derecha else izquierda
        return None
    if op == '*':
        if izquierda == 'String' and derecha == 'i32':
            return 'String'
        if izquierda == 'i32' and derecha == 'String':
            return 'String'
        if izquierda in NUMERICOS and derecha in NUMERICOS:
            return 'f64' if izquierda != derecha else izquierda
        return None
    if op in ('/', '%'):
        if izquierda in NUMERICOS and derecha in NUMERICOS:
            return 'f64' if izquierda != derecha else izquierda
        return None
    return None
