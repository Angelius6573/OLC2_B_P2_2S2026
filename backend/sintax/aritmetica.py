from backend.analizador_lexico import tokens

from backend.ast_modular.aritmetica import OperacionBinaria, Variable, NumeroEntero, NumeroFloat

def p_operacion(t):
    '''operacion : operacion MINUS operadores_multiplicativos
                 | operacion ADD operadores_multiplicativos
                 | operadores_multiplicativos
    '''
    if len(t) == 2:
        t[0] = t[1]
    if len(t) == 4:
        t[0] = OperacionBinaria(izquierda=t[1], operador=t[2], derecha=t[3])

def p_operadores_multiplicativos(t):
    '''operadores_multiplicativos : operadores_multiplicativos MULTI operando
                                  | operadores_multiplicativos DIV operando
                                  | operadores_multiplicativos MOD operando
                                  | operando
    '''
    if len(t) == 2:
        t[0] = t[1]
    if len(t) == 4:
        match t.slice[2].type:
            case 'MULTI':
                t[0] = OperacionBinaria(izquierda=t[1], operador=t[2], derecha=t[3])
            case 'DIV':
                t[0] = OperacionBinaria(izquierda=t[1], operador=t[2], derecha=t[3])
            case 'MOD':
                t[0] = OperacionBinaria(izquierda=t[1], operador=t[2], derecha=t[3])

def p_operando(t):
    '''operando : ID
                | NUMERO_ENTERO
                | NUMERO_FLOAT
                | OPEN_PAR operacion CLOSE_PAR
    '''
    match t.slice[1].type:
        case 'ID':
            t[0] = Variable(id=t[1])
        case 'NUMERO_ENTERO':
            t[0] = NumeroEntero(valor=t[1])
        case 'NUMERO_FLOAT':
            t[0] = NumeroFloat(valor=t[1])
        case 'OPEN_PAR':
            t[0] = t[2] # No nos interesan los parentesis
        case _:
            print(f"Token inesperado: {t.slice[1].type}")


