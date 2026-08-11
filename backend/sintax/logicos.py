from backend.analizador_lexico import tokens

from backend.ast_modular.aritmetica import OperacionBinaria, OperacionUnaria

def p_operacion_logica(t):
    '''operacion_logica : operacion_logica OR operacion_logica_and
                        | operacion_logica_and
    '''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = OperacionBinaria(izquierda=t[1], operador=t[2], derecha=t[3])

def p_operacion_logica_and(t):
    '''operacion_logica_and : operacion_logica_and AND operacion_logica_not
                            | operacion_logica_not
    '''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = OperacionBinaria(izquierda=t[1], operador=t[2], derecha=t[3])

def p_operacion_logica_not(t):
    '''operacion_logica_not : NOT operacion_logica_not
                            | operacion_relacional
    '''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = OperacionUnaria(operador=t[1], derecha=t[2])

def p_corto_circuito(t):
    '''corto_circuito : operacion_logica
    '''
    t[0] = t[1]
