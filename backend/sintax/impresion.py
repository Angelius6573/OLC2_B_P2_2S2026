from backend.analizador_lexico import tokens

# Todo lo que no es 'argumentos_impresion' es azúcar sintáctico, lo sacamos del análisis
def p_sentencia_imprimir(t):
    'sentencia_imprimir : PRINTLN OPEN_PAR argumentos_impresion CLOSE_PAR SEMICOLON'
    t[0] = ('IMPRIMIR', t[3])

def p_argumentos_impresion(t):
    '''argumentos_impresion : CADENA
                            | CADENA COMMA operaciones_directas
    '''
    if len(t) == 2:
        t[0] = ('CONTENIDO', t[1], [])
    if len(t) == 4:
        t[0] = ('CONTENIDO', t[1], t[3])

def p_operaciones_directas(t):
    '''operaciones_directas : operaciones_directas COMMA operacion
                            | operacion
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    if len(t) == 4:
        t[1].append(t[3])
        t[0] = t[1]
    # Se devuelve siempre una lista de expresiones. Por recursividad se acumula en la misma lista
