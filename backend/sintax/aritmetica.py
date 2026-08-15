from backend.analizador_lexico import tokens

from backend.ast_modular.aritmetica import OperacionBinaria, OperacionUnaria, Variable, NumeroEntero, NumeroFloat, Cadena
from backend.ast_modular.arrays import AccederIndice, Slice
from backend.ast_modular.funciones_embebidas import FuncionEmbebida
from backend.ast_modular.struct import AccederCampo

def p_operacion_aritmetica(t):
    '''operacion_aritmetica : operacion_aritmetica MINUS operadores_multiplicativos
                            | operacion_aritmetica ADD operadores_multiplicativos
                            | operadores_multiplicativos
    '''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = OperacionBinaria(izquierda=t[1], operador=t[2], derecha=t[3])

def p_operadores_multiplicativos(t):
    '''operadores_multiplicativos : operadores_multiplicativos DIV operacion_unaria
                                  | operadores_multiplicativos MOD operacion_unaria
                                  | operadores_multiplicativos MULTI operacion_unaria
                                  | operacion_unaria
    '''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = OperacionBinaria(izquierda=t[1], operador=t[2], derecha=t[3])

def p_operacion_unaria(t):
    '''operacion_unaria : MINUS operacion_unaria %prec NEGACION_UNARIA
                        | operando
    '''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = OperacionUnaria(operador=t[1], derecha=t[2])

def p_operando(t):
    '''operando : ID
                | NUMERO_ENTERO
                | NUMERO_FLOAT
                | CARACTER
                | CADENA
                | RAWSTRING
                | booleano
                | nuevo_array
                | typeof_var
                | random_var
                | llamar_funcion
                | slice_var
                | OPEN_PAR operacion_aritmetica CLOSE_PAR
    '''
    match t.slice[1].type:
        case 'ID':
            t[0] = Variable(id=t[1])
        case 'NUMERO_ENTERO':
            t[0] = NumeroEntero(valor=t[1])
        case 'NUMERO_FLOAT':
            t[0] = NumeroFloat(valor=t[1])
        case 'CADENA':
            t[0] = Cadena(string=t[1])
        case 'OPEN_PAR':
            t[0] = t[2] # No nos interesan los parentesis
        case _:
            t[0] = t[1] # El resto de alternativas ya construyen su propio nodo

def p_operando_acceder_campo(t):
    'operando : operando DOT ID'
    t[0] = AccederCampo(objetivo=t[1], campo=t[3])

def p_operando_acceder_indice(t):
    'operando : operando OPEN_BRACKET seleccionar_indice CLOSE_BRACKET'
    t[0] = AccederIndice(objetivo=t[1], indices=[t[3]])

def p_operando_len(t):
    'operando : operando DOT LEN OPEN_PAR CLOSE_PAR'
    t[0] = FuncionEmbebida(nombre='len', objetivo=t[1], argumentos=[])

def p_operando_replace(t):
    'operando : operando DOT REPLACE OPEN_PAR CADENA COMMA CADENA CLOSE_PAR'
    t[0] = FuncionEmbebida(
        nombre='replace',
        objetivo=t[1],
        argumentos=[Cadena(string=t[5]), Cadena(string=t[7])]
    )

def p_operando_to_uppercase(t):
    'operando : operando DOT MAYUSCULAS OPEN_PAR CLOSE_PAR'
    t[0] = FuncionEmbebida(nombre='to_uppercase', objetivo=t[1], argumentos=[])

def p_operando_to_lowercase(t):
    'operando : operando DOT MINUSCULAS OPEN_PAR CLOSE_PAR'
    t[0] = FuncionEmbebida(nombre='to_lowercase', objetivo=t[1], argumentos=[])

def p_operando_contains(t):
    'operando : operando DOT CONTAINS OPEN_PAR CADENA CLOSE_PAR'
    t[0] = FuncionEmbebida(
        nombre='contains',
        objetivo=t[1],
        argumentos=[Cadena(string=t[5])]
    )

def p_operando_split(t):
    'operando : operando DOT SPLIT OPEN_PAR CADENA CLOSE_PAR'
    t[0] = FuncionEmbebida(
        nombre='split',
        objetivo=t[1],
        argumentos=[Cadena(string=t[5])]
    )

def p_operando_reverse(t):
    'operando : operando DOT REVERSE OPEN_PAR CLOSE_PAR'
    t[0] = FuncionEmbebida(nombre='reverse', objetivo=t[1], argumentos=[])

def p_slice_var(t):
    'slice_var : AMPERSAND ID OPEN_BRACKET seleccionar_indice RANGE seleccionar_indice CLOSE_BRACKET'
    t[0] = Slice(
        objetivo=Variable(id=t[2]),
        inicio=t[4],
        fin=t[6]
    )


