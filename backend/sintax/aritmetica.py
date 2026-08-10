from backend.analizador_lexico import tokens

from backend.ast_modular.aritmetica import OperacionBinaria, OperacionUnaria, Variable, NumeroEntero, NumeroFloat, Cadena

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
                | CADENA
                | typeof_var
                | random_var
                | len_var
                | replace_var
                | to_upp_var
                | to_low_var
                | llamar_funcion
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
            print(f"Token inesperado: {t.slice[1].type}")


