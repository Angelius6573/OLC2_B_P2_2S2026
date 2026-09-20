from backend.ast_modular.aritmetica import (NumeroEntero, NumeroFloat, Cadena, Caracter, Booleano)

ARITMETICOS = ('+', '-', '*', '/', '%')

def _es_numerico(val):
    return isinstance(val, (int, float)) and not isinstance(val, bool)

def _incompatibles(op, izq, der):
    if op == '+':
        return not (_es_numerico(izq) and _es_numerico(der)) and \
               not (isinstance(izq, str) and isinstance(der, str))
    if op == '*':
        return not ((_es_numerico(izq) and _es_numerico(der)) or
                    (isinstance(izq, str) and _es_numerico(der)) or
                    (_es_numerico(izq) and isinstance(der, str)))
    return not (_es_numerico(izq) and _es_numerico(der))

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
    if op in ARITMETICOS:
        if getattr(nodo, 'tipo', None) is None or _incompatibles(op, izq, der):
            return None
    try:
        if op == '+':
            return izq + der
        if op == '-':
            return izq - der
        if op == '*':
            return izq * der
        if op == '/':
            if der == 0:
                raise RuntimeError(f"{nodo.linea}:{nodo.columna} División por cero")
            resultado = izq / der
            if isinstance(izq, int) and isinstance(der, int) and resultado == int(resultado):
                return int(resultado)
            return resultado
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
    except TypeError:
        return None
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
