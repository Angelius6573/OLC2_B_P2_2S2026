from backend.analizador_lexico import tokens

def p_operacion_logica(t):
    '''operacion_logica : operacion_logica OR operacion_logica_and
                        | operacion_logica_and
    '''

def p_operacion_logica_and(t):
    '''operacion_logica_and : operacion_logica_and AND operacion_logica_not
                            | operacion_logica_not
    '''

def p_operacion_logica_not(t):
    '''operacion_logica_not : NOT operacion_logica_not
                            | operacion_relacional
    '''

def p_corto_circuito(t):
    '''corto_circuito : operacion_logica SEMICOLON
    '''
