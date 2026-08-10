from backend.analizador_lexico import tokens

def p_instanciar_struct(t):
    'instanciar_struct : ID OPEN_BRACE params_struct CLOSE_BRACE'

def p_params_struct(t):
    '''params_struct : params_struct param_struct
                     | param_struct
    '''

def p_param_struct(t):
    'param_struct : ID COLON expresion COMMA'

def p_asignar_params_struct(t):
    '''asignar_params_struct : asignar_params_struct DOT ID
                             | ID
    '''
