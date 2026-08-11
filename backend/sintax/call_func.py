from backend.analizador_lexico import tokens

from backend.ast_modular.funciones import LlamadaFuncion

def p_llamar_funcion(t):
    'llamar_funcion : nombre_func_called OPEN_PAR params_func_called CLOSE_PAR'
    t[0] = LlamadaFuncion(nombre_funcion=t[1], parametros=t[3])

def p_nombre_func_called(t):
    '''nombre_func_called : ID
                          | MAIN
    '''
    t[0] = t[1]

def p_params_func_called(t):
    '''params_func_called : params_func_called COMMA parametro_call
                          | parametro_call
                          | empty
    '''
    if len(t) == 4:
        t[1].append(t[3])
        t[0] = t[1]
    elif t[1] is not None:
        t[0] = [t[1]]
    else:
        t[0] = []

def p_parametro_call(t):
    '''parametro_call : operando
    '''
    t[0] = t[1]
