from backend.analizador_lexico import tokens
from backend.ast_modular.variables import Asignacion, DeclaracionVariable

def p_declaracion_variable(t):
    'declaracion_variable : var_mutable ID tipo_declaracion'
    tipo, valor = t[3]
    t[0] = DeclaracionVariable(
        nombre=t[2],
        mutabilidad=t[1],
        tipo=tipo,
        valor=valor
    )

def p_var_mutable(t):
    '''var_mutable : LET
                   | LET MUT
    '''
    t[0] = 'let' if len(t) == 2 else 'let mut'

def p_tipo_declaracion(t):
    '''tipo_declaracion : var_implicita
                        | var_explicita
    '''
    t[0] = t[1]

def p_var_implicita(t):
    'var_implicita : ASSIGN valor'
    t[0] = (None, t[2])

def p_var_explicita(t):
    '''var_explicita : COLON tipo_dato
                     | COLON tipo_dato ASSIGN valor
    '''
    if len(t) == 3:
        t[0] = (t[2], None)
    else:
        t[0] = (t[2], t[4])

def p_asignacion_variable(t):
    'asignacion_variable : ID ASSIGN valor SEMICOLON'
    t[0] = Asignacion(nombre=t[1], valor=t[3])
