from backend.analizador_lexico import tokens

# Devuelve String
def p_typeof_var(t):
    'typeof_var : TYPEOF OPEN_PAR obtener_tipo CLOSE_PAR'

# Devuelve i32
def p_random_var(t):
    'random_var : RANDOM OPEN_PAR only_enteros COMMA only_enteros CLOSE_PAR'

# Devuelve i32
def p_len_var(t):
    '''len_var : ID DOT LEN OPEN_PAR CLOSE_PAR
               | literales DOT LEN OPEN_PAR CLOSE_PAR
    '''

# Devuelve bool
def p_contains_var(t):
    'contains_var : ID DOT CONTAINS OPEN_PAR CADENA CLOSE_PAR'

# Devuelve String
def p_replace_var(t):
    'replace_var : ID DOT REPLACE OPEN_PAR CADENA COMMA CADENA CLOSE_PAR'

# Devuelve Array
def p_split_var(t):
    'split_var : ID DOT SPLIT OPEN_PAR CADENA CLOSE_PAR'

# Devuelve String
def p_to_upp_var(t):
    'to_upp_var : ID DOT MAYUSCULAS OPEN_PAR CLOSE_PAR'

# Devuelve String
def p_to_low_var(t):
    'to_low_var : ID DOT MINUSCULAS OPEN_PAR CLOSE_PAR'

# Devuelve Array
def p_reverse_var(t):
    'reverse_var : ID DOT REVERSE OPEN_PAR CLOSE_PAR'

def p_obtener_tipo(t):
    '''obtener_tipo : ID
                    | literales
    '''
