from types import SimpleNamespace

from backend.ast_modular.aritmetica import (
    OperacionBinaria, OperacionUnaria, Variable,
    NumeroEntero, NumeroFloat, Cadena, Caracter, Booleano,
)
from backend.checker.helpers import binaria, operador_invalido, no_declarada, se_esperaba, es_literal
from backend.checker.tipos import NUMERICOS

def _en_operador(nodo):
    # Los errores de una operación binaria apuntan a su operador
    linea, columna = getattr(nodo, 'posicion_operador', (nodo.linea, nodo.columna))
    return SimpleNamespace(linea=linea, columna=columna)

def _aritmetica_invalida(self, nodo, operador, izquierda, derecha):
    # Con un solo operando literal, el problema es el tipo de ese literal: x + "5"
    if es_literal(nodo.derecha) != es_literal(nodo.izquierda):
        literal, otro = (derecha, izquierda) if es_literal(nodo.derecha) else (izquierda, derecha)
        se_esperaba(self, _en_operador(nodo), otro, literal)
    else:
        operador_invalido(self, _en_operador(nodo), operador, izquierda, derecha)

def visitar_OperacionBinaria(self, nodo):
    izquierda = self.visitar(nodo.izquierda)
    derecha = self.visitar(nodo.derecha)
    operador = nodo.operador
    if izquierda is None or derecha is None:
        return None
    if operador in ('+', '-', '*', '/', '%'):
        tipo = binaria(operador, izquierda, derecha)
        if tipo is None:
            _aritmetica_invalida(self, nodo, operador, izquierda, derecha)
            nodo.tipo = None
            return None
    elif operador in ('==', '!=', '<', '<=', '>', '>='):
        if izquierda == derecha or (izquierda in NUMERICOS and derecha in NUMERICOS):
            tipo = 'bool'
        else:
            operador_invalido(self, _en_operador(nodo), operador, izquierda, derecha)
            tipo = 'bool'
    elif operador in ('&&', '||'):
        if izquierda == 'bool' and derecha == 'bool':
            tipo = 'bool'
        else:
            operador_invalido(self, _en_operador(nodo), operador, izquierda, derecha)
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
            self.error(nodo.linea, nodo.columna, f"No es posible aplicar el operador '!' a un valor de tipo {derecha}.")
            tipo = 'bool'
    else:
        if derecha in NUMERICOS:
            tipo = derecha
        else:
            self.error(nodo.linea, nodo.columna, f"No es posible aplicar el operador '-' a un valor de tipo {derecha}.")
            tipo = 'i32'
    nodo.tipo = tipo
    return tipo

def visitar_Variable(self, nodo):
    simbolo = self.tabla.buscar_variable(nodo.id)
    if simbolo is None:
        no_declarada(self, nodo, nodo.id)
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
