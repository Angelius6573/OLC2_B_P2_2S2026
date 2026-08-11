from backend.analizador_lexico import tokens
from backend.ast_modular.arrays import AccederIndice
from backend.ast_modular.aritmetica import Variable

def p_nuevo_array(t):
    'nuevo_array : OPEN_BRACKET arrays CLOSE_BRACKET'
    if t[2] is None:
        t[0] = []
    else:
        t[0] = t[2]

def p_arrays(t):
    '''arrays : arrays COMMA operando
              | operando
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[3])
        t[0] = t[1]

def p_tipo_array(t):
    'tipo_array : OPEN_BRACKET tipo_dato SEMICOLON NUMERO_ENTERO CLOSE_BRACKET'
    t[0] = f'[{t[2]}; {t[4]}]'

def p_acceder_indice_array(t):
    'acceder_indice_array : ID posiciones_array'
    t[0] = AccederIndice(objetivo=Variable(id=t[1]), indices=t[2])

def p_posiciones_array(t):
    '''posiciones_array : posiciones_array OPEN_BRACKET seleccionar_indice CLOSE_BRACKET
                        | OPEN_BRACKET seleccionar_indice CLOSE_BRACKET
    '''
    if len(t) == 5:
        t[1].append(t[3])
        t[0] = t[1]
    else:
        t[0] = [t[2]]

def p_seleccionar_indice(t):
    '''seleccionar_indice : operacion_aritmetica
    '''
    t[0] = t[1]
