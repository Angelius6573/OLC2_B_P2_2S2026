from backend.analizador_lexico import tokens

from backend.ast_modular.aritmetica import Cadena, Variable
from backend.ast_modular.funciones_embebidas import FuncionEmbebida

# Devuelve String
def p_typeof_var(t):
    'typeof_var : TYPEOF OPEN_PAR obtener_tipo CLOSE_PAR'
    t[0] = FuncionEmbebida(nombre='typeof', argumentos=[t[3]])

# Devuelve i32
def p_random_var(t):
    'random_var : RANDOM OPEN_PAR only_enteros COMMA only_enteros CLOSE_PAR'
    t[0] = FuncionEmbebida(nombre='random', argumentos=[t[3], t[5]])

# Devuelve i32
def p_len_var(t):
    '''len_var : ID DOT LEN OPEN_PAR CLOSE_PAR
               | operando DOT LEN OPEN_PAR CLOSE_PAR
    '''
    if t.slice[1].type == 'ID':
        t[0] = FuncionEmbebida(nombre='len', objetivo=Variable(id=t[1]))
    else:
        t[0] = FuncionEmbebida(nombre='len', objetivo=t[1])

# Devuelve bool
def p_contains_var(t):
    'contains_var : ID DOT CONTAINS OPEN_PAR CADENA CLOSE_PAR'
    t[0] = FuncionEmbebida(
        nombre='contains',
        objetivo=Variable(id=t[1]),
        argumentos=[Cadena(string=t[5])]
    )

# Devuelve String
def p_replace_var(t):
    'replace_var : ID DOT REPLACE OPEN_PAR CADENA COMMA CADENA CLOSE_PAR'
    t[0] = FuncionEmbebida(
        nombre='replace',
        objetivo=Variable(id=t[1]),
        argumentos=[Cadena(string=t[5]), Cadena(string=t[7])]
    )

# Devuelve Array
def p_split_var(t):
    'split_var : ID DOT SPLIT OPEN_PAR CADENA CLOSE_PAR'
    t[0] = FuncionEmbebida(
        nombre='split',
        objetivo=Variable(id=t[1]),
        argumentos=[Cadena(string=t[5])]
    )

# Devuelve String
def p_to_upp_var(t):
    'to_upp_var : ID DOT MAYUSCULAS OPEN_PAR CLOSE_PAR'
    t[0] = FuncionEmbebida(nombre='to_uppercase', objetivo=Variable(id=t[1]))

# Devuelve String
def p_to_low_var(t):
    'to_low_var : ID DOT MINUSCULAS OPEN_PAR CLOSE_PAR'
    t[0] = FuncionEmbebida(nombre='to_lowercase', objetivo=Variable(id=t[1]))

# Devuelve Array
def p_reverse_var(t):
    'reverse_var : ID DOT REVERSE OPEN_PAR CLOSE_PAR'
    t[0] = FuncionEmbebida(nombre='reverse', objetivo=Variable(id=t[1]))

def p_obtener_tipo(t):
    '''obtener_tipo : operando
    '''
    t[0] = t[1]
