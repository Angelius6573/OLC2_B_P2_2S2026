from backend.analizador_lexico import contar_columna

def fijar_ubicacion(t, nodo, pos=1):
    for simbolo in t.slice[pos:]:
        if hasattr(simbolo, 'lineno'):
            nodo.linea = simbolo.lineno
            nodo.columna = contar_columna(t.lexer.lexdata, simbolo)
            return nodo
        valor = getattr(simbolo, 'value', None)
        if isinstance(valor, list) and valor and getattr(valor[0], 'linea', None) is not None:
            nodo.linea = valor[0].linea
            nodo.columna = getattr(valor[0], 'columna', None)
            return nodo
        if getattr(valor, 'linea', None) is not None:
            nodo.linea = valor.linea
            nodo.columna = getattr(valor, 'columna', None)
            return nodo
    return nodo
