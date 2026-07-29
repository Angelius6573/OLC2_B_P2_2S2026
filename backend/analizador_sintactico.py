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
