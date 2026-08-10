from backend.analizador_lexico import tokens

def p_llamar_funcion(t):
    'llamar_funcion : nombre_func_called OPEN_PAR params_func_called CLOSE_PAR'

def p_nombre_func_called(t):
    '''nombre_func_called : ID
                          | MAIN
    '''

def p_params_func_called(t):
    '''params_func_called : params_func_called COMMA parametro_call
                          | parametro_call
                          | empty
    '''

def p_parametro_call(t):
    '''parametro_call : ID
                      | literales
    '''
