from backend.analizador_lexico import tokens

def p_decString(t):
    'decString : DT_STRING COLON COLON tipo_dec_string'

def p_tipo_dec_string(t):
    '''tipo_dec_string : from_directo
                       | new_posterior
    '''

def p_from_directo(t):
    'from_directo : FROMSTRING OPEN_PAR tipo_cadena CLOSE_PAR SEMICOLON'

def p_new_posterior(t):
    'new_posterior : NEWSTRING OPEN_PAR CLOSE_PAR SEMICOLON'

def p_asignar_valor_string(t):
    'asignar_valor_string : ID DOT PUSH_STR OPEN_PAR tipo_cadena CLOSE_PAR SEMICOLON'

def p_tipo_cadena(t):
    '''tipo_cadena : CADENA
                   | RAWSTRING
    '''
