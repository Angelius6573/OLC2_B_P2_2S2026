import ply.lex as lex
import ply.yacc as yacc
from backend.analizador_lexico import lexema_tipo, lexer, linea_columna, tokens
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
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUAL', 'NO_EQUAL', 'GTE', 'LTE', 'GT', 'LT'),
    ('left', 'ADD', 'MINUS'),
    ('left', 'MULTI', 'DIV', 'MOD'),
    ('right', 'NOT', 'NEGACION_UNARIA') # NEGACION_UNARIA es un token invent solo para la precedencia, sigue siendo el "-"
)

def tokens_esperados():
    estado = getattr(parser, 'state', None)
    if estado is None:
        return set()
    return {tok for tok in parser.action.get(estado, {}) if tok not in ('error', '$end')}

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

# Cierres en orden de prioridad: si falta uno al final de una línea, el error va tras el token anterior
_CIERRES = (('SEMICOLON', ';'), ('CLOSE_BRACE', '}'), ('CLOSE_PAR', ')'), ('CLOSE_BRACKET', ']'))
# Con más opciones que estas, la lista de esperados no ayuda a corregir
_MAXIMO_SUGERIDOS = 3

def _sugerencia(esperados):
    if not esperados or len(esperados) > _MAXIMO_SUGERIDOS:
        return ''
    nombres = sorted(f"'{lexema_tipo(nombre)}'" for nombre in esperados)
    lista = nombres[0] if len(nombres) == 1 else ', '.join(nombres[:-1]) + ' o ' + nombres[-1]
    return f' Se esperaba {lista}.'

def p_error(t):
    datos = lexer.lexdata
    esperados = tokens_esperados()
    anterior = lexer.token_anterior
    cierre = next((lexema for nombre, lexema in _CIERRES if nombre in esperados), None)
    salto_de_linea = anterior is not None and (t is None or '\n' in datos[anterior.fin:t.lexpos])
    if cierre and salto_de_linea:
        linea, columna = linea_columna(datos, anterior.fin)
        reportar('Sintactico', linea, columna, f"Se esperaba '{cierre}'.")
    elif t is None:
        linea, columna = linea_columna(datos, anterior.fin) if anterior else (1, 1)
        reportar('Sintactico', linea, columna, f'Fin de archivo inesperado.{_sugerencia(esperados)}')
    else:
        linea, columna = linea_columna(datos, t.lexpos)
        reportar('Sintactico', linea, columna,
                 f"Token inesperado '{datos[t.lexpos:t.fin]}'.{_sugerencia(esperados)}")

parser = yacc.yacc(start='init')

def analizar(codigo):
    """Parsea el programa. Si el archivo termina con llaves abiertas (por ejemplo, porque un comentario
    sin cierre se comió la última), reporta la que falta y la cierra con un '}' implícito: sin eso, PLY
    abandona en el fin de archivo y el programa no llega al análisis semántico ni a la ejecución."""
    abiertas = 0
    ultimo = None
    reportado = False

    def siguiente():
        nonlocal abiertas, ultimo, reportado
        token = lexer.token()
        if token is not None:
            abiertas += {'OPEN_BRACE': 1, 'CLOSE_BRACE': -1}.get(token.type, 0)
            ultimo = token
            return token
        if abiertas <= 0 or ultimo is None:
            return None
        if not reportado:
            reportar('Sintactico', *linea_columna(lexer.lexdata, ultimo.fin), "Se esperaba '}'.")
            reportado = True
        abiertas -= 1
        cierre = lex.LexToken()
        cierre.type, cierre.value = 'CLOSE_BRACE', '}'
        cierre.lineno, cierre.lexpos = ultimo.lineno, len(lexer.lexdata)
        cierre.fin = cierre.lexpos
        return cierre

    return parser.parse(codigo, lexer=lexer, tokenfunc=siguiente)
