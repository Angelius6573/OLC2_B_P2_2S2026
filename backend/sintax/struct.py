from backend.analizador_lexico import tokens
from backend.ast_modular.struct import DeclaracionStruct, Parametros
from backend.sintax.helpers import fijar_ubicacion

def p_declaracion_struct(t):
    'declaracion_struct : STRUCT ID bloque_struct'
    t[0] = fijar_ubicacion(t, DeclaracionStruct(
        nombre_struct=t[2],
        parametros_struct=t[3]
    ))

def p_bloque_struct(t):
    'bloque_struct : OPEN_BRACE contenido_struct CLOSE_BRACE'
    t[0] = t[2]

def p_contenido_struct(t):
    '''contenido_struct : lista_campos_struct
                        | lista_campos_struct COMMA
    '''
    t[0] = t[1]

def p_lista_campos_struct(t):
    '''lista_campos_struct : parametros_struct
                           | lista_campos_struct COMMA parametros_struct
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[3])
        t[0] = t[1]

def p_parametros_struct(t):
    'parametros_struct : ID COLON td_parametro_struct'
    t[0] = fijar_ubicacion(t, Parametros(
        parametro=t[1],
        tipo_parametro=t[3]
    ))

def p_td_parametro_struct(t):
    '''td_parametro_struct : ID
                           | tipo_dato
    '''
    t[0] = t[1]
