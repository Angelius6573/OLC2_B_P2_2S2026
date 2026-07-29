import ply.yacc as yacc

from analizador_lexico import tokens

precedencia = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUAL', 'NO_EQUAL', 'GTE', 'LTE', 'GT', 'LT'),
    ('left', 'ADD', 'MINUS'),
    ('left', 'MULTI', 'DIV', 'MOD'),
    ('right', 'NOT', 'NEGACION_UNARIA') # NEGACION_UNARIA es un token invent solo para la precedencia, sigue siendo el -
)

def p_init(t):
    'init : Programa'
    t[0] = t[1]

def p_Programa(t):
    '''Programa : Programa Sentencia
            | Sentencia
    '''

def p_Sentencia(t):
    '''Sentencia : Sentencia Imprimir
                 | Imprimir
    '''

def p_Imprimir(t):
    'Imprimir: PRINTLN OPEN_PAR ArgumentosImpresion CLOSE_PAR SEMICOLON'

def p_ArgumentosImpresion(t):
    '''ArgumentosImpresion : ArgumentosImpresion COMMA Expresion
                           | CadenaFormato
    '''

def p_CadenaFormat(t):
    'CadenaFormato : CADENA'

def p_Expresion(t):
    '''Expresion : Expresion ADD Termino
                 | Expresion MINUS Termino
                 | Termino
    '''

def p_Termino(t):
    '''Termino : Termino MULTI Factor
               | Factor
    '''

def p_Factor(t):
    '''Factor : ID
              | NUMERO_ENTERO
              | NUMERO_FLOAT
              | OPEN_PAR Expresion CLOSE_PAR
    '''
