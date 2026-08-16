import ply.lex as lex
from itertools import chain

from backend.errores import reportar

reserved_words = {
    'fn' : 'FUNCTION',
    'let' : 'LET',
    'main' : 'MAIN',
    'mut' : 'MUT',
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
    'false' : 'FALSE',
    'String' : 'DT_STRING',
    'i32' : 'DT_INT',
    'f64' : 'DT_FLOAT',
    'bool' : 'DT_BOOL',
    'char' : 'DT_CHARACTER',
    'from' : 'FROMSTRING',
    'new' : 'NEWSTRING',
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
    'push_str' : 'PUSH_STR'
}

match_tokens = {
    'FAT_ARROW' : r'=>',
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
    'AMPERSAND' : r'&',
}

# Con esto se deshace el código repetitivo de los for para cada array
for token, patron in chain(match_tokens.items(),
                           relationals.items(),
                           logics.items(),
                           assignments.items(),
                           arithmetics.items(),
                           delimiters.items(),
                           punctuators.items()):
    globals()[f't_{token}'] = patron

# Lista de tuplas de los tokens, nombre y ER
conjunto_tokens = list(chain(
    match_tokens.keys(),
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
    'RAWSTRING',
    'PRINTLN',
    'MATCH_BASE',
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

def t_RAWSTRING(t):
    r'r\#"([^"]|"(?!\#))*"\#|r"[^"]*"'
    if t.value.startswith('r#"'):
        t.value = t.value[3:-2]   ## r#"{contenido}"# → contenido
    else:
        t.value = t.value[2:-1]   ## r"{contenido}" -> contenido
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

def t_MATCH_BASE(t):
    r'_(?![a-zA-Z0-9_])'
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

def contar_columna(input, token):
    linea = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - linea) + 1

LEXEMA_TIPO = {
    **{v: k for k, v in reserved_words.items()},
    **{v: k for k, v in embedded_functions.items()},
    **{nombre: patron.replace('\\', '') for nombre, patron in chain(
        match_tokens.items(),
        relationals.items(),
        logics.items(),
        assignments.items(),
        arithmetics.items(),
        delimiters.items(),
        punctuators.items())},
    'PRINTLN': 'println!',
    'MATCH_BASE': '_',
    'ID': 'identificador',
    'NUMERO_ENTERO': 'número entero',
    'NUMERO_FLOAT': 'número decimal',
    'CARACTER': 'carácter',
    'CADENA': 'cadena',
    'RAWSTRING': 'cadena cruda',
}

def lexema_tipo(tipo):
    return LEXEMA_TIPO.get(tipo, tipo)

def t_error(t):
    reportar('Lexico', t.lineno, contar_columna(t.lexer.lexdata, t), f"Carácter no reconocido '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
# lexer = lex.lex(reflags = re.IGNORECASE) <- En caso de que un error de importación de lexico a sintáctico, maybe hay que tener esto

# PLY no reinicia el lineno al llamar input(); sin esto, parses consecutivos
# en el mismo proceso acumulan número de línea.
_input_original = lexer.input
def input_con_lineno_reset(data):
    lexer.lineno = 1
    return _input_original(data)
lexer.input = input_con_lineno_reset
