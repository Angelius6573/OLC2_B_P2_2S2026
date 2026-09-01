import ply.yacc as yacc
from backend.analizador_lexico import contar_columna, lexema_tipo, lexer, tokens
from backend.errores import reportar

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
from backend.sintax.helpers import fijar_ubicacion
from backend.sintax.logicos import *
from backend.sintax.match import *
from backend.sintax.relacionales import *
from backend.sintax.struct import *
from backend.sintax.variables import *

from backend.ast import Programa
from backend.ast_modular.aritmetica import Booleano, NumeroEntero, Variable

precedence = (
    ('left', 'AND'),
    ('left', 'OR'),
    ('left', 'EQUAL', 'NO_EQUAL', 'GTE', 'LTE', 'GT', 'LT'),
    ('left', 'MULTI', 'MINUS'),
    ('left', 'ADD', 'DIV', 'MOD'),
    ('right', 'NOT', 'NEGACION_UNARIA') # NEGACION_UNARIA es un token invent solo para la precedencia, sigue siendo el "-"
)

def tokens_esperados():
    estado = getattr(parser, 'state', None)
    if estado is None:
        return 'nada'
    acciones = parser.action.get(estado, {})
    nombres = sorted(tok for tok in acciones if tok not in ('error', '$end'))
    if not nombres:
        return 'nada'
    return " o ".join(lexema_tipo(nombre) for nombre in nombres)

def p_init(t):
    'init : programa'
    t[0] = fijar_ubicacion(t, Programa(declaraciones=t[1]))

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

def p_declaracion_global_error(t):
    'declaracion_global : error'
    t[0] = None

# Se agrega ID porque los structs mueren, es mejor sintetizarlos como tipos de datos y listo
def p_tipo_dato(t):
    '''tipo_dato : ID
                 | DT_INT
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
                 | match_expr
    '''
    t[0] = t[1]

def p_booleano(t):
    '''booleano : TRUE
                | FALSE
    '''
    t[0] = fijar_ubicacion(t, Booleano(valor=t[1] == 'true'))

def p_only_enteros(t):
    '''only_enteros : ID
                    | NUMERO_ENTERO
    '''
    if t.slice[1].type == 'ID':
        t[0] = fijar_ubicacion(t, Variable(id=t[1]))
    else:
        t[0] = fijar_ubicacion(t, NumeroEntero(valor=t[1]))

def p_empty(t):
    'empty :'
    t[0] = None

_SYNC_TOKENS = {
    'LET', 'IF', 'WHILE', 'FOR', 'LOOP', 'PRINTLN',
    'RETURN', 'STRUCT', 'FUNCTION', 'MATCH', 'BREAK', 'CONTINUE',
    'CLOSE_BRACE', 'EOF',
}

def p_error(t):
    if t:
        columna = contar_columna(t.lexer.lexdata, t)
        reportar('Sintactico', t.lineno, columna,
                 f"Se esperaba '{tokens_esperados()}' pero se encontró '{t.value}'")
    else:
        reportar('Sintactico', lexer.lineno, 0,
                 f"Se esperaba '{tokens_esperados()}' pero se encontró 'nada'")

parser = yacc.yacc(start='init')
