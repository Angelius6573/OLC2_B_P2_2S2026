from backend.analizador_lexico import tokens

from backend.ast_modular.funciones_embebidas import FuncionEmbebida
from backend.sintax.helpers import fijar_ubicacion

# Devuelve String
def p_typeof_var(t):
    'typeof_var : TYPEOF OPEN_PAR obtener_tipo CLOSE_PAR'
    t[0] = fijar_ubicacion(t, FuncionEmbebida(nombre='typeof', argumentos=[t[3]]))

# Devuelve i32
def p_random_var(t):
    'random_var : RANDOM OPEN_PAR only_enteros COMMA only_enteros CLOSE_PAR'
    t[0] = fijar_ubicacion(t, FuncionEmbebida(nombre='random', argumentos=[t[3], t[5]]))

def p_obtener_tipo(t):
    '''obtener_tipo : operando
    '''
    t[0] = t[1]
