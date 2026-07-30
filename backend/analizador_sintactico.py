from operator import le

import ply.yacc as yacc
from backend.analizador_lexico import tokens

precedencia = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUAL', 'NO_EQUAL', 'GTE', 'LTE', 'GT', 'LT'),
    ('left', 'ADD', 'MINUS'),
    ('left', 'MULTI', 'DIV', 'MOD'),
    ('right', 'NOT', 'NEGACION_UNARIA') # NEGACION_UNARIA es un token invent solo para la precedencia, sigue siendo el "-"
)

def p_init(t):
    'init : programa'
    t[0] = t[1] # reasignar a ('PROGRAMA', t[1]) después para el AST
    #t[0] = ('PROGRAMA', t[1])

# programa siempre espera una lista de tuplas, esto es conveniente
# a la hora de desarrollar el AST
def p_programa(t):
    '''programa : programa instruccion
                | instruccion
    '''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    if len(t) == 2:
        t[0] = [t[1]] if t[1] is not None else []

# instruccion actua a modo de enrutador en la gramática, de modo que podemos seguir agregando
# sentencias sin preocuparnos por reasignar a t[0] en cada caso
def p_instruccion(t):
    '''instruccion : sentencia_imprimir
                   | declaracion_funcion
                   | empty
    '''
    t[0] = t[1]

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

# Todo lo que no es 'argumentos_impresion' es azúcar sintáctico, lo sacamos del análisis
def p_sentencia_imprimir(t):
    'sentencia_imprimir : PRINTLN OPEN_PAR argumentos_impresion CLOSE_PAR punto_coma'
    t[0] = ('IMPRIMIR', t[3])

def p_argumentos_impresion(t):
    '''argumentos_impresion : CADENA
                           | CADENA COMMA lista_expresion
    '''
    if len(t) == 2:
        t[0] = ('CONTENIDO', t[1], [])
    if len(t) == 4:
        t[0] = ('CONTENIDO', t[1], t[3])

def p_punto_coma(t):
    '''punto_coma : SEMICOLON
                  | empty
    '''
    t[0] = t[1] if len(t) == 2 else None

def p_lista_expresion(t):
    '''lista_expresion : expresion
                       | lista_expresion COMMA expresion
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    if len(t) == 4:
        t[1].append(t[3])
        t[0] = t[1]
    # Se devuelve siempre una lista de expresiones. Por recursividad se acumula en la misma lista

def p_expresion(t):
    '''expresion : expresion MINUS termino
                 | expresion ADD termino
                 | termino
    '''
    if len(t) == 2:
        t[0] = t[1]
    if len(t) == 4:
        t[0] = ('BINARIA', t[1], t[2], t[3])

def p_termino(t):
    '''termino : termino MULTI factor
               | termino DIV factor
               | termino MOD factor
               | factor
    '''
    if len(t) == 2:
        t[0] = t[1]
    if len(t) == 4:
        t[0] = ('BINARIA', t[1], t[2], t[3])

def p_factor(t):
    '''factor : ID
              | NUMERO_ENTERO
              | NUMERO_FLOAT
              | OPEN_PAR expresion CLOSE_PAR
    '''
    match t.slice[1].type:
        case 'ID':
            t[0] = ('VARIABLE', t[1])
        case 'NUMERO_ENTERO':
            t[0] = ('i32', t[1])
        case 'NUMERO_FLOAT':
            t[0] = ('f64', t[1])
        case 'OPEN_PAR':
            t[0] = t[2] # No nos interesan los parentesis
        case _:
            print(f"Token inesperado: {t.slice[1].type}")

def p_empty(t):
    'empty :'
    t[0] = None
    pass

def p_error(t):
    if t:
        print(f"Error sintáctico en '{t.value}' línea {t.lineno}")
    else:
        print("Error sintáctico: EOF inesperado")

parser = yacc.yacc()
