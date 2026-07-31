import ply.yacc as yacc
from backend.analizador_lexico import tokens

from backend.sintax.funciones import *
from backend.sintax.impresion import *
from backend.sintax.aritmetica import *

from backend.ast import Programa

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUAL', 'NO_EQUAL', 'GTE', 'LTE', 'GT', 'LT'),
    ('left', 'ADD', 'MINUS'),
    ('left', 'MULTI', 'DIV', 'MOD'),
    ('right', 'NOT', 'NEGACION_UNARIA') # NEGACION_UNARIA es un token invent solo para la precedencia, sigue siendo el "-"
)

def p_init(t):
    'init : programa'
    #t[0] = t[1] # reasignar a ('PROGRAMA', t[1]) después para el AST
    #t[0] = ('PROGRAMA', t[1])
    t[0] = Programa(declaraciones=t[1])

# programa siempre espera una lista de tuplas, esto es conveniente
# a la hora de desarrollar el AST
def p_programa(t):
    '''programa : programa declaracion_global
                | declaracion_global
    '''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    if len(t) == 2:
        t[0] = [t[1]] if t[1] is not None else []

# agregar 'declaracion_struct' cuando sea posible
def p_declaracion_global(t):
    'declaracion_global : declaracion_funcion'
    t[0] = t[1]

def p_tipo_dato(t):
    '''tipo_dato : DT_INT
                 | DT_FLOAT
                 | DT_BOOL
                 | DT_CHARACTER
                 | DT_STRING
    '''
    t[0] = t[1]

def p_empty(t):
    'empty :'
    t[0] = None

def p_error(t):
    if t:
        print(f"Error sintáctico en '{t.value}' línea {t.lineno}")
    else:
        print("Error sintáctico: EOF inesperado")

parser = yacc.yacc(start='init')
