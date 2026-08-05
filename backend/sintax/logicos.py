from backend.analizador_lexico import tokens

def p_operadores_logicos(t):
    '''operadores_logicos : operadores_logicos EQUAL operador_logico
                          | operadores_logicos NO_EQUAL operador_logico
                          | operadores_logicos GTE operador_logico
                          | operadores_logicos LTE operador_logico
                          | operadores_logicos GT operador_logico
                          | operadores_logicos LT operador_logico
    '''

def p_operador_logico(t):
    '''operador_logico : ID
                       | booleano
                       | NUMERO_ENTERO
                       | NUMERO_FLOAT
                       | OPEN_PAR operadores_logicos CLOSE_PAR
    '''
