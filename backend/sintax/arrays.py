from backend.analizador_lexico import tokens

def p_nuevo_array(t):
    '''nuevo_array : OPEN_BRACKET arrays CLOSE_BRACKET
                   | OPEN_BRACKET NUMERO_ENTERO SEMICOLON NUMERO_ENTERO CLOSE_BRACKET
    '''
    if len(t) == 6:
        t[0] = [t[2]] * t[4]
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
