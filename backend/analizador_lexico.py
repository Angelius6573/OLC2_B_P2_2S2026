import ply.lex as lex
from itertools import chain

reserved_words = {
    'fn' : 'FUNCTION',
    'let' : 'VAR_DECLARED',
    'mut' : 'MUTABILITY',
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR',
    'in' : 'FOR_IN',
    'loop' : 'LOOP',
    'match' : 'MATCH',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'return' : 'RETURN',
    'struct' : 'STRUCT',
    'true' : 'TRUE',
    'false' : 'false',
    'String' : 'DT_STRING',
    'i32' : 'DT_INT',
    'f64' : 'DT_FLOAT',
    'bool' : 'DT_BOOL',
    'char' : 'DT_CHARACTER',
}

embedded_functions = {
    'typeof' : 'TYPEOF',
    'random' : 'RANDOM',
    'len' : 'LEN',
    'contains': 'CONTAINS',
    'replace' : 'REPLACE',
    'split' : 'SPLIT',
    'to_uppercase' : 'MAYUSCULAS',
    'to_lowercase' : 'MINUSCULAS',
    'reverse' : 'REVERSE',
}

# Primero los tokens que cuyo lexema tenga una longitud mayor que 1
relationals = {
    'EQUAL' : r'==',
    'NO_EQUAL' : r'!=',
    'GTE' : r'>=',
    'LTE' : r'<=',
    'GT' : r'>',
    'LT' : r'<',
}

logics = {
    'AND' : r'&&',
    'OR' : r'\|\|',
    'NOT' : r'!',
}

assignments = {
    'RETURN_TYPE' : r'->',
    'ADD_ASSIGN' : r'\+=',
    'MINUS_ASSIGN' : r'-=',
    'MULTI_ASSIGN' : r'\*=',
    'DIV_ASSIGN' : r'/=',
    'MOD_ASSIGN' : r'%=',
    'ASSIGN' : r'=',
}

arithmetics = {
    'ADD' : r'\+',
    'MINUS' : r'-',
    'MULTI' : r'\*',
    'DIV' : r'/',
    'MOD' : r'%',
}

delimiters = {
    'OPEN_PAR' : r'\(',
    'CLOSE_PAR' : r'\)',
    'OPEN_BRACE' : r'\{',
    'CLOSE_BRACE' : r'\}',
    'OPEN_BRACKET' : r'\[',
    'CLOSE_BRACKET' : r'\]',
}

punctuators = {
    'RANGE' : r'\.\.',
    'DOT' : r'\.',
    'COMMA' : r'\,',
    'COLON' : r':',
    'SEMICOLON' : r'\;',
}

# Con esto se deshace el código repetitivo de los for para cada array
for token, patron in chain(relationals.items(),
                           logics.items(),
                           assignments.items(),
                           arithmetics.items(),
                           delimiters.items(),
                           punctuators.items()):
    globals()[f't_{token}'] = patron

# Lista de tuplas de los tokens, nombre y ER
conjunto_tokens = list(chain(
    relationals.keys(),
    logics.keys(),
    assignments.keys(),
    arithmetics.keys(),
    delimiters.keys(),
    punctuators.keys()
))

conjunto_reservados = {**reserved_words, **embedded_functions}

tokens = (
    *conjunto_reservados.values(),
    *conjunto_tokens,
    'NUMERO_ENTERO',
    'NUMERO_FLOAT',
    'CARACTER',
    'CADENA',
    'PRINTLN',
    'ID',
)

def t_PRINTLN(t):
    r'println!'
    return t

def t_CADENA(t):
    r'\"([^\\\"]|\\.)*\"'
    t.value = t.value[1:-1] # Remover comillas
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\"', '\"')
    t.value = t.value.replace("\\'", "\'")
    t.value = t.value.replace('\\\\', '\\')
    return t

def t_CARACTER(t):
    r"'([^'\\]|\\.)'"
    t.value = eval(t.value)
    return t

def t_NUMERO_FLOAT(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Valor f64 muy grande %d", t.value)
        t.value = 0
    return t

def t_NUMERO_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Valor i32 muy grande %d", t.value)
        t.value = 0
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = conjunto_reservados.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_ignore_COMENTARIO_UNA_LINEA(t):
    r'//.*'
    pass

def t_ignore_COMENTARIO_MULTI_LINEA(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print("Carácter no permitido '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
