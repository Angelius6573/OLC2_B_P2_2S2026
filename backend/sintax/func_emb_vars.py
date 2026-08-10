from backend.analizador_lexico import tokens

def p_typeof_var(t):
    'typeof_var : TYPEOF OPEN_PAR ID CLOSE_PAR'

def p_random_var(t):
    'random_var : RANDOM OPEN_PAR only_enteros COMMA only_enteros CLOSE_PAR'

def p_len_var(t):
    'len_var : ID DOT LEN OPEN_PAR CLOSE_PAR'

def p_contains_var(t):
    'contains_var : ID DOT CONTAINS OPEN_PAR CADENA CLOSE_PAR'

def p_replace_var(t):
    'replace_var : ID DOT REPLACE OPEN_PAR CADENA COMMA CADENA CLOSE_PAR'

def p_split_var(t):
    'split_var : ID DOT SPLIT OPEN_PAR CADENA CLOSE_PAR'

def p_to_upp_var(t):
    'to_upp_var : ID MAYUSCULAS SPLIT OPEN_PAR CADENA CLOSE_PAR'

def p_to_low_var(t):
    'to_low_var : ID MINUSCULAS SPLIT OPEN_PAR CADENA CLOSE_PAR'

def p_reverse_var(t):
    'reverse_var : ID DOT REVERSE OPEN_PAR CLOSE_PAR'
