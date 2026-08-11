from backend.analizador_lexico import tokens
from backend.ast_modular.aritmetica import Variable
from backend.ast_modular.struct import AccederCampo, AsignarParametro, InstanciarStruct

def p_instanciar_struct(t):
    'instanciar_struct : ID OPEN_BRACE params_struct CLOSE_BRACE'
    t[0] = InstanciarStruct(nombre=t[1], parametros=t[3])

def p_params_struct(t):
    '''params_struct : params_struct param_struct
                     | param_struct
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]

def p_param_struct(t):
    'param_struct : ID COLON expresion COMMA'
    t[0] = AsignarParametro(nombre=t[1], valor=t[3])

def p_asignar_params_struct(t):
    '''asignar_params_struct : asignar_params_struct DOT ID
                             | ID DOT ID
    '''
    if len(t) == 4:
        t[0] = AccederCampo(objetivo=t[1], campo=t[3])
    else:
        t[0] = AccederCampo(objetivo=Variable(id=t[1]), campo=t[3])
