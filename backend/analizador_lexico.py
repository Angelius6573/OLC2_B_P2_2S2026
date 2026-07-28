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
    'OR' : r'||',
    'NOT' : r'!',
}

assignments = {
    'RETURN_TYPE' : r'->',
    'ADD_ASSIGN' : r'\+=',
    'MINUS_ASSIGN' : r'-=',
    'MULTI_ASSIGN' : r'\*=',
    'DIV_ASSIGN' : r'/=',
    'MOD_ASSIGN' : r'%=',
}

arithmetics = {
    'ADD' : r'\+',
    'MINUS' : r'-',
    'MULTI' : r'\*',
    'DIV' : r'/',
    'MOD' : r'%',
    'ASSIGN' : r'=',
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

tokens = (
    *reserved_words.values(),
    *conjunto_tokens,
    'NUMERO_ENTERO',
    'ID',
)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_ignore_COMENTARIO_UNA_LINEA(t):
    r'//.*'
    pass

def t_ignore_COMENTARIO_MULTI_LINEA(t):
    r'(?s)/\*.*?\*/'
    # (?s) : Python's flag (Inline flag), hace que el punto de vista coincida con cualquier carácter
    #        incluyendo los saltos de línea
    # /\*  : Detecta el inicio del comentario /*
    # .*?  : El signo de cuantificación opcional es clave, hace que la búsqueda no sea greedy con la búsqueda del cierre,
    #        cualquier * le vale para intentar cerrar el comentario. De tal modo que cierra en el primer */ que encuentre
    #        De otro modo, el parser consumirá todos los carácteres hasta el fin del documento o hasta encontrar otro comentario.
    # \*/  : Detecta el cierre del comentario */
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print("Carácter no permitido '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
