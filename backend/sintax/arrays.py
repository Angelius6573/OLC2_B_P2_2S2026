from backend.analizador_lexico import tokens
from backend.ast_modular.arrays import AccederIndice, AsignarIndice, Repetidor

def p_nuevo_array(t):
    '''nuevo_array : OPEN_BRACKET arrays CLOSE_BRACKET
                   | OPEN_BRACKET valor SEMICOLON operacion_aritmetica CLOSE_BRACKET
    '''
    if len(t) == 6:
        t[0] = Repetidor(valor=t[2], cantidad=t[4])
    elif t[2] is None:
        t[0] = []
    else:
        t[0] = t[2]

def p_arrays(t):
    '''arrays : arrays COMMA valor
              | valor
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[3])
        t[0] = t[1]

def p_tipo_array(t):
    'tipo_array : OPEN_BRACKET tipo_dato SEMICOLON NUMERO_ENTERO CLOSE_BRACKET'
    t[0] = f'[{t[2]}; {t[4]}]'

def p_seleccionar_indice(t):
    '''seleccionar_indice : operacion_aritmetica
    '''
    t[0] = t[1]

def p_asignacion_indice(t):
    '''asignacion_indice : operando OPEN_BRACKET seleccionar_indice CLOSE_BRACKET ASSIGN valor SEMICOLON
                         | operando OPEN_BRACKET seleccionar_indice CLOSE_BRACKET OPEN_BRACKET seleccionar_indice CLOSE_BRACKET ASSIGN valor SEMICOLON
    '''
    if len(t) == 8:
        objetivo = AccederIndice(objetivo=t[1], indices=[t[3]])
        valor = t[6]
    else:
        objetivo = AccederIndice(
            objetivo=AccederIndice(objetivo=t[1], indices=[t[3]]),
            indices=[t[6]]
        )
        valor = t[9]
    t[0] = AsignarIndice(objetivo=objetivo, valor=valor)
