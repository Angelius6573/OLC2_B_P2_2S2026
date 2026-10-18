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

def fijar_operador(t, nodo):
    """Ubicación de una operación binaria t[1] op t[3]. Además guarda la del operador, que es donde
    apuntan sus errores semánticos, como en el ejemplo de tipos incompatibles del enunciado."""
    fijar_ubicacion(t, nodo)
    operador = t.slice[2]
    nodo.posicion_operador = (operador.lineno, contar_columna(t.lexer.lexdata, operador))
    return nodo
