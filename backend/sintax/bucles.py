from backend.analizador_lexico import tokens

from backend.ast_modular.aritmetica import Variable
from backend.ast_modular.bucles import BucleWhile, BucleLoop, BucleFor, Rango, Break, Continue
from backend.sintax.helpers import fijar_ubicacion

def p_bucle_while(t):
    'bucle_while : WHILE expresion bloque_ambito'
    t[0] = fijar_ubicacion(t, BucleWhile(condicion=t[2], bloque_ambito=t[3]))

def p_bucle_loop(t):
    'bucle_loop : LOOP bloque_ambito'
    t[0] = fijar_ubicacion(t, BucleLoop(bloque_ambito=t[2]))

def p_bucle_for(t):
    'bucle_for : FOR ID FOR_IN rango_for bloque_ambito'
    t[0] = fijar_ubicacion(t, BucleFor(variable=fijar_ubicacion(t, Variable(id=t[2]), 2), iterable=t[4], bloque_ambito=t[5]))

def p_rango_for(t):
    '''rango_for : operacion_aritmetica
                 | operacion_aritmetica RANGE operacion_aritmetica
    '''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = fijar_ubicacion(t, Rango(inicio=t[1], fin=t[3]))

def p_break_stmt(t):
    'break_stmt : BREAK SEMICOLON'
    t[0] = fijar_ubicacion(t, Break())

def p_continue_stmt(t):
    'continue_stmt : CONTINUE SEMICOLON'
    t[0] = fijar_ubicacion(t, Continue())
