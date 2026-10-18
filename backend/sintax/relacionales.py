from backend.analizador_lexico import tokens

from backend.ast_modular.aritmetica import OperacionBinaria
from backend.sintax.helpers import fijar_operador

def p_operacion_relacional(t):
    '''operacion_relacional : operacion_relacional EQUAL operador_relacional
                            | operacion_relacional NO_EQUAL operador_relacional
                            | operacion_relacional GTE operador_relacional
                            | operacion_relacional LTE operador_relacional
                            | operacion_relacional GT operador_relacional
                            | operacion_relacional LT operador_relacional
                            | operador_relacional
    '''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = fijar_operador(t, OperacionBinaria(izquierda=t[1], operador=t[2], derecha=t[3]))

def p_operador_relacional(t):
    # Entre paréntesis cabe una expresión lógica completa: (a && b) || c
    '''operador_relacional : operacion_aritmetica
                           | OPEN_PAR operacion_logica CLOSE_PAR
    '''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = t[2]
