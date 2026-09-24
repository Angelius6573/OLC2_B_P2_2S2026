from backend.ast_modular.aritmetica import (
    OperacionBinaria, OperacionUnaria, Variable,
    NumeroEntero, NumeroFloat, Cadena, Caracter, Booleano,
)
from backend.checker.helpers import se_esperaba, binaria
from backend.checker.tipos import NUMERICOS

def visitar_OperacionBinaria(self, nodo):
    izquierda = self.visitar(nodo.izquierda)
    derecha = self.visitar(nodo.derecha)
    operador = nodo.operador
    if izquierda is None or derecha is None:
        return None
    if operador in ('+', '-', '*', '/', '%'):
        tipo = binaria(operador, izquierda, derecha)
        if tipo is None:
            self.error(nodo.linea, nodo.columna,
                       f"No es posible aplicar el operador '{operador}' entre los tipos {izquierda} y {derecha}.")
            nodo.tipo = None
            return None
    elif operador in ('==', '!=', '<', '<=', '>', '>='):
        if izquierda == derecha or (izquierda in NUMERICOS and derecha in NUMERICOS):
            tipo = 'bool'
        else:
            se_esperaba(self, nodo, 'mismos tipos',
                        f'{izquierda} {operador} {derecha}')
            tipo = 'bool'
    elif operador in ('&&', '||'):
        if izquierda == 'bool' and derecha == 'bool':
            tipo = 'bool'
        else:
            se_esperaba(self, nodo, 'bool', f'{izquierda} {operador} {derecha}')
            tipo = 'bool'
    else:
        return None
    nodo.tipo = tipo
    return tipo

def visitar_OperacionUnaria(self, nodo):
    derecha = self.visitar(nodo.derecha)
    if derecha is None:
        return None
    if nodo.operador == '!':
        if derecha == 'bool':
            tipo = 'bool'
        else:
            se_esperaba(self, nodo, 'bool', derecha)
            tipo = 'bool'
    else:
        if derecha in NUMERICOS:
            tipo = derecha
        else:
            se_esperaba(self, nodo, 'número', derecha)
            tipo = 'i32'
    nodo.tipo = tipo
    return tipo

def visitar_Variable(self, nodo):
    simbolo = self.tabla.buscar_variable(nodo.id)
    if simbolo is None:
        self.error(nodo.linea, nodo.columna,
                   f"Variable '{nodo.id}' utilizada no fue declarada")
        return None
    nodo.tipo = simbolo.tipo
    nodo.sym_id = simbolo.sym_id
    return simbolo.tipo

def visitar_NumeroEntero(self, nodo):
    nodo.tipo = 'i32'
    return 'i32'

def visitar_NumeroFloat(self, nodo):
    nodo.tipo = 'f64'
    return 'f64'

def visitar_Cadena(self, nodo):
    nodo.tipo = 'String'
    return 'String'

def visitar_Caracter(self, nodo):
    nodo.tipo = 'char'
    return 'char'

def visitar_Booleano(self, nodo):
    nodo.tipo = 'bool'
    return 'bool'
