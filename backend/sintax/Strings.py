from backend.analizador_lexico import tokens
from backend.ast_modular.Strings import DeclaracionString
from backend.ast_modular.aritmetica import Cadena
from backend.ast_modular.funciones_embebidas import FuncionEmbebida

def p_decString(t):
    'decString : DT_STRING COLON COLON tipo_dec_string'
    t[0] = t[4]

def p_tipo_dec_string(t):
    '''tipo_dec_string : from_directo
                       | new_posterior
    '''
    t[0] = t[1]

def p_from_directo(t):
    'from_directo : FROMSTRING OPEN_PAR tipo_cadena CLOSE_PAR'
    t[0] = DeclaracionString(metodo='from', valor=Cadena(string=t[3]))

def p_new_posterior(t):
    'new_posterior : NEWSTRING OPEN_PAR CLOSE_PAR'
    t[0] = DeclaracionString(metodo='new', valor=None)

def p_asignar_valor_string(t):
    'asignar_valor_string : operando DOT PUSH_STR OPEN_PAR tipo_cadena CLOSE_PAR'
    t[0] = FuncionEmbebida(
        nombre='push_str',
        objetivo=t[1],
        argumentos=[Cadena(string=t[5])]
    )

def p_tipo_cadena(t):
    '''tipo_cadena : CADENA
                   | RAWSTRING
    '''
    t[0] = t[1]
