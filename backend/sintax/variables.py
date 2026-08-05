from backend.analizador_lexico import tokens

def p_declaracion_variable(t):
    'declaracion_variable : var_mutable ID tipo_declaracion'

def p_var_mutable(t):
    '''var_mutable : LET
                   | LET MUT
    '''

def p_tipo_declaracion(t):
    '''tipo_declaracion : var_implicita
                        | var_explicita
    '''

def p_var_implicita(t):
    'var_implicita : ASSIGN expresion'

def p_var_explicita(t):
    '''var_explicita : ASSIGN decString
                     | COLON tipo_dato
                     | COLON tipo_dato ASSIGN expresion
    '''
