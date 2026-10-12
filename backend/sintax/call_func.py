from backend.analizador_lexico import tokens

from backend.ast_modular.funciones import LlamadaFuncion
from backend.sintax.helpers import fijar_ubicacion

def p_llamar_funcion(t):
    'llamar_funcion : nombre_func_called OPEN_PAR params_func_called CLOSE_PAR'
    t[0] = fijar_ubicacion(t, LlamadaFuncion(nombre_funcion=t[1], parametros=t[3]))

def p_nombre_func_called(t):
    '''nombre_func_called : ID
                          | MAIN
    '''
    t[0] = t[1]
    # Sin esto, fijar_ubicacion salta este no terminal y la llamada queda en el '('
    t.set_lineno(0, t.lineno(1))
    t.set_lexpos(0, t.lexpos(1))

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
    '''parametro_call : valor
    '''
    t[0] = t[1]
