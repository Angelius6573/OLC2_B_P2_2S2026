from backend.ast_modular.aritmetica import Variable
from backend.ast_modular.arrays import AccederIndice
from backend.checker.tipos import LITERALES, NUMERICOS, TIPOS_PRIMITIVOS

def es_literal(nodo):
    return isinstance(nodo, LITERALES)

# Textos de los errores semánticos con la redacción del enunciado §3.5.1
def se_esperaba(analizador, nodo, esperado, obtenido):
    analizador.error(nodo.linea, nodo.columna, f"Tipos incompatibles. No es posible utilizar un valor de tipo "
                                               f"{obtenido} donde se esperaba un valor de tipo {esperado}.")

def operador_invalido(analizador, nodo, operador, izquierda, derecha):
    analizador.error(nodo.linea, nodo.columna,
                     f"No es posible aplicar el operador '{operador}' entre los tipos {izquierda} y {derecha}.")

def no_declarada(analizador, nodo, nombre):
    analizador.error(nodo.linea, nodo.columna, f"La variable '{nombre}' no ha sido declarada.")

def inmutable(analizador, nodo, nombre):
    analizador.error(nodo.linea, nodo.columna,
                     f"No es posible modificar la variable '{nombre}' porque fue declarada como inmutable.")

def verificar_asignacion(analizador, nodo, tipo, tipo_valor):
    if tipo == tipo_valor:
        return
    # La columna es la del valor, como en el ejemplo del enunciado (§3.5.1, caso 5)
    ubicacion = nodo.valor if getattr(nodo.valor, 'linea', None) is not None else nodo
    analizador.error(ubicacion.linea, ubicacion.columna,
                     f"No es posible asignar un valor de tipo {tipo_valor} a una variable de tipo {tipo}.")

def verificar_tipo_definido(analizador, tipo, nodo):
    if tipo in TIPOS_PRIMITIVOS or tipo.startswith('[') or tipo.startswith('&'):
        return
    if analizador.tabla.buscar_struct(tipo) is not None:
        return
    analizador.error(nodo.linea, nodo.columna, f"El tipo '{tipo}' no está definido.")

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
