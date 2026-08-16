from backend.analizador_lexico import tokens
from backend.ast_modular.funciones import DeclaracionFuncion, NombreFuncion, Return
from backend.sintax.helpers import fijar_ubicacion

def p_declaracion_funcion(t):
    'declaracion_funcion : FUNCTION nombre_funcion OPEN_PAR parametros_funcion CLOSE_PAR valor_retorno bloque_ambito'
    t[0] = fijar_ubicacion(t, DeclaracionFuncion(
        nombre_funcion=t[2],
        parametros_funcion=t[4],
        valor_retorno=t[6],
        bloque_ambito=t[7]
    ))

def p_nombre_funcion(t):
    '''nombre_funcion : ID
                      | MAIN
    '''
    match t.slice[1].type:
        case 'ID':
            t[0] = fijar_ubicacion(t, NombreFuncion(nombre_conjunto='FUNC', nombre_funcion=t[1]))
        case 'MAIN':
            t[0] = fijar_ubicacion(t, NombreFuncion(nombre_conjunto='ENTRY_POINT', nombre_funcion=t[1]))
        case _:
            print(f"Token inesperado: {t.slice[1].type}")

def p_parametros_funcion(t):
    '''parametros_funcion : parametros_funcion COMMA ID COLON tipo_dato
                          | ID COLON tipo_dato
                          | empty
    '''
    if len(t) == 6:
        t[1].append(t[3])
        t[1].append(t[5])
        t[0] = t[1]
    elif len(t) == 4:
        t[0] = [t[1], t[3]]
    else:
        t[0] = []

def p_valor_retorno(t):
    '''valor_retorno : empty
                     | RETURN_TYPE tipo_dato
    '''
    if len(t) == 3:
        t[0] = t[2]
    else:
        t[0] = []

def p_bloque_ambito(t):
    'bloque_ambito : OPEN_BRACE instrucciones CLOSE_BRACE'
    t[0] = t[2]

def p_instrucciones(t):
    '''instrucciones : instrucciones instruccion
                     | instruccion
                     | empty
    '''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    if len(t) == 2:
        t[0] = [t[1]] if t[1] is not None else []

# instruccion actua a modo de enrutador en la gramática, de modo que podemos seguir agregando
# sentencias sin preocuparnos por reasignar a t[0] en cada caso
def p_instruccion(t):
    '''instruccion : sentencia_imprimir SEMICOLON
                   | llamar_funcion SEMICOLON
                   | declaracion_variable SEMICOLON
                   | corto_circuito SEMICOLON
                   | asignar_valor_string SEMICOLON
                   | asignacion_variable
                   | asignacion_indice
                   | condicional
                   | bucle_while
                   | bucle_loop
                   | bucle_for
                   | return_stmt
                   | break_stmt
                   | continue_stmt
    '''
    t[0] = t[1]

def p_return_stmt(t):
    '''return_stmt : RETURN expresion SEMICOLON
                   | RETURN SEMICOLON
    '''
    if len(t) == 4:
        t[0] = fijar_ubicacion(t, Return(valor=t[2]))
    else:
        t[0] = fijar_ubicacion(t, Return(valor=None))
