from backend.analizador_lexico import tokens
from backend.ast_modular.struct import AsignarParametro, InstanciarStruct
from backend.sintax.helpers import fijar_ubicacion

def p_instanciar_struct(t):
    '''instanciar_struct : ID OPEN_BRACE params_struct CLOSE_BRACE
                         | ID OPEN_BRACE params_struct COMMA CLOSE_BRACE
    '''
    t[0] = fijar_ubicacion(t, InstanciarStruct(nombre=t[1], parametros=t[3]))

def p_params_struct(t):
    '''params_struct : params_struct COMMA param_struct
                     | param_struct
                     | empty
    '''
    if len(t) == 2:
        t[0] = [t[1]] if t[1] is not None else []
    else:
        t[1].append(t[3])
        t[0] = t[1]

def p_param_struct(t):
    'param_struct : ID COLON valor'
    t[0] = fijar_ubicacion(t, AsignarParametro(nombre=t[1], valor=t[3]))

# instanciar_struct ya no vive dentro de operando/expresion (evita la ambiguedad `ID {`
# con el bloque del if/while). Se expone solo donde se espera un valor.
def p_valor(t):
    '''valor : expresion
             | instanciar_struct
    '''
    t[0] = t[1]


