import ply.yacc as yacc
from backend.analizador_lexico import tokens

from backend.sintax.Strings import *
from backend.sintax.aritmetica import *
from backend.sintax.arrays import *
from backend.sintax.bucles import *
from backend.sintax.call_func import *
from backend.sintax.condicionales import *
from backend.sintax.func_emb_vars import *
from backend.sintax.funciones import *
from backend.sintax.impresion import *
from backend.sintax.instance_struct import *
from backend.sintax.logicos import *
from backend.sintax.relacionales import *
from backend.sintax.struct import *
from backend.sintax.variables import *

from backend.ast import Programa
from backend.ast_modular.aritmetica import NumeroEntero, Variable

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
    t[0] = Programa(declaraciones=t[1])

# programa siempre espera una lista de tuplas, esto es conveniente
# a la hora de desarrollar el AST
def p_programa(t):
    '''programa : programa declaracion_global
                | declaracion_global
                | empty
    '''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    if len(t) == 2:
        t[0] = [t[1]] if t[1] is not None else []

# agregar 'declaracion_struct' cuando sea posible
def p_declaracion_global(t):
    '''declaracion_global : declaracion_funcion
                          | declaracion_struct
    '''
    t[0] = t[1]

def p_tipo_dato(t):
    '''tipo_dato : DT_INT
                 | DT_FLOAT
                 | DT_BOOL
                 | DT_CHARACTER
                 | DT_STRING
                 | tipo_array
    '''
    t[0] = t[1]

def p_expresion(t):
    '''expresion : operacion_logica
                 | decString
    '''
    t[0] = t[1]

def p_booleano(t):
    '''booleano : TRUE
                | FALSE
    '''
    t[0] = t[1]

def p_only_enteros(t):
    '''only_enteros : ID
                    | NUMERO_ENTERO
    '''
    if t.slice[1].type == 'ID':
        t[0] = Variable(id=t[1])
    else:
        t[0] = NumeroEntero(valor=t[1])

def p_empty(t):
    'empty :'
    t[0] = None

def p_error(t):
    if t:
        print(f"Error sintáctico en '{t.value}' línea {t.lineno}")
    else:
        print("Error sintáctico: EOF inesperado")

parser = yacc.yacc(start='init')
