from backend.analizador_lexico import tokens

from backend.ast_modular.match import Match, MatchCase, MatchBase
from backend.ast_modular.aritmetica import NumeroEntero, NumeroFloat, Caracter, Cadena
from backend.sintax.helpers import fijar_ubicacion

def p_match_expr(t):
    'match_expr : MATCH expresion OPEN_BRACE match_brazos CLOSE_BRACE'
    t[0] = fijar_ubicacion(t, Match(expresion=t[2], brazos=t[4]))

def p_match_brazos(t):
    '''match_brazos : match_brazos COMMA match_brazo
                    | match_brazos COMMA
                    | match_brazo
                    | empty
    '''
    if len(t) == 4:
        t[1].append(t[3])
        t[0] = t[1]
    elif len(t) == 3:
        t[0] = t[1]
    elif t[1] is not None:
        t[0] = [t[1]]
    else:
        t[0] = []

def p_match_brazo(t):
    'match_brazo : match_patron FAT_ARROW match_cuerpo'
    t[0] = fijar_ubicacion(t, MatchCase(patron=t[1], cuerpo=t[3]))

def p_match_cuerpo(t):
    '''match_cuerpo : expresion
                    | sentencia_imprimir
    '''
    t[0] = t[1]

def p_match_patron(t):
    '''match_patron : NUMERO_ENTERO
                    | NUMERO_FLOAT
                    | CARACTER
                    | CADENA
                    | RAWSTRING
                    | booleano
                    | MATCH_BASE
    '''
    if t.slice[1].type == 'MATCH_BASE':
        t[0] = fijar_ubicacion(t, MatchBase())
    elif t.slice[1].type == 'NUMERO_ENTERO':
        t[0] = fijar_ubicacion(t, NumeroEntero(valor=t[1]))
    elif t.slice[1].type == 'NUMERO_FLOAT':
        t[0] = fijar_ubicacion(t, NumeroFloat(valor=t[1]))
    elif t.slice[1].type == 'CARACTER':
        t[0] = fijar_ubicacion(t, Caracter(valor=t[1]))
    elif t.slice[1].type in ('CADENA', 'RAWSTRING'):
        t[0] = fijar_ubicacion(t, Cadena(string=t[1]))
    else:
        t[0] = t[1]
