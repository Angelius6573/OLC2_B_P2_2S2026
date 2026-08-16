from backend.analizador_lexico import tokens

from backend.ast_modular.condicionales import Condicional
from backend.sintax.helpers import fijar_ubicacion

def p_condicional(t):
    '''condicional : IF expresion bloque_ambito
                   | IF expresion bloque_ambito ELSE bloque_ambito
                   | IF expresion bloque_ambito ELSE condicional
    '''
    if len(t) == 4:
        t[0] = fijar_ubicacion(t, Condicional(condicion=t[2], bloque_verdadero=t[3], bloque_falso=None))
    else:
        t[0] = fijar_ubicacion(t, Condicional(condicion=t[2], bloque_verdadero=t[3], bloque_falso=t[5]))
