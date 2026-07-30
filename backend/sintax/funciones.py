from backend.analizador_lexico import tokens

def p_declaracion_funcion(t):
    'declaracion_funcion : FUNCTION ID OPEN_PAR parametros_funcion CLOSE_PAR bloque_ambito'
    t[0] = ('FUNCION', t[2], t[4], t[6])

def p_parametros_funcion(t):
    '''parametros_funcion : parametros_funcion COMMA ID
                          | ID
                          | empty
    '''
    if len(t) == 4:
        t[1].append(t[3])
        t[0] = t[1]
    elif len(t) == 2:
        t[0] = [t[1]] if t[1] is not None else []

def p_bloque_ambito(t):
    'bloque_ambito : OPEN_BRACE lista_instrucciones CLOSE_BRACE'
    t[0] = t[2]

def p_lista_instrucciones(t):
    '''lista_instrucciones : lista_instrucciones instruccion
                           | instruccion
    '''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    if len(t) == 2:
        t[0] = [t[1]] if t[1] is not None else []
