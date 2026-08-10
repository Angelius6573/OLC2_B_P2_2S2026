from backend.analizador_lexico import tokens

def p_operacion_relacional(t):
    '''operacion_relacional : operacion_relacional EQUAL operador_relacional
                            | operacion_relacional NO_EQUAL operador_relacional
                            | operacion_relacional GTE operador_relacional
                            | operacion_relacional LTE operador_relacional
                            | operacion_relacional GT operador_relacional
                            | operacion_relacional LT operador_relacional
                            | operador_relacional
    '''

def p_operador_relacional(t):
    '''operador_relacional : ID
                           | booleano
                           | operacion_aritmetica
                           | OPEN_PAR operacion_relacional CLOSE_PAR
    '''
