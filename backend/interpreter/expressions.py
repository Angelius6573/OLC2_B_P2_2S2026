from backend.ast_modular.aritmetica import (NumeroEntero, NumeroFloat, Cadena, Caracter, Booleano)

def visitar_NumeroEntero(self, nodo):
    return nodo.valor

def visitar_NumeroFloat(self, nodo):
    return nodo.valor

def visitar_Cadena(self, nodo):
    return nodo.string

def visitar_Caracter(self, nodo):
    return nodo.valor

def visitar_Booleano(self, nodo):
    return nodo.valor

def visitar_OperacionBinaria(self, nodo):
    izq = self.visitar(nodo.izquierda)
    der = self.visitar(nodo.derecha)
    op = nodo.operador
    if op == '+':
        return izq + der
    if op == '-':
        return izq - der
    if op == '*':
        return izq * der
    if op == '/':
        if der == 0:
            raise RuntimeError(f"{nodo.linea}:{nodo.columna} División por cero")
        return izq / der
    if op == '%':
        if der == 0:
            raise RuntimeError(f"{nodo.linea}:{nodo.columna} Módulo por cero")
        return izq % der
    if op == '==':
        return izq == der
    if op == '!=':
        return izq != der
    if op == '<':
        return izq < der
    if op == '<=':
        return izq <= der
    if op == '>':
        return izq > der
    if op == '>=':
        return izq >= der
    if op == '&&':
        return izq and der
    if op == '||':
        return izq or der
    return None

def visitar_OperacionUnaria(self, nodo):
    der = self.visitar(nodo.derecha)
    if nodo.operador == '-':
        return -der
    if nodo.operador == '!':
        return not der
    return None

def visitar_Variable(self, nodo):
    v = self.ambito_actual.buscar(nodo.id)
    if v is None:
        raise RuntimeError(f"{nodo.linea}:{nodo.columna} Variable '{nodo.id}' no declarada")
    return v.valor
