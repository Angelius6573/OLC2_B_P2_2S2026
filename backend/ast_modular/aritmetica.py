from backend.ast import Nodo

class OperacionBinaria(Nodo):
    def __init__(self, izquierda, operador, derecha):
        super().__init__()
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha

class OperacionUnaria(Nodo):
    def __init__(self, operador, derecha):
        super().__init__()
        self.operador = operador
        self.derecha = derecha

class Variable(Nodo):
    def __init__(self, id):
        super().__init__()
        self.id = str(id)

class NumeroEntero(Nodo):
    def __init__(self, valor):
        super().__init__()
        self.valor = int(valor)

class NumeroFloat(Nodo):
    def __init__(self, valor):
        super().__init__()
        self.valor = float(valor)

class Cadena(Nodo):
    def __init__(self, string):
        super().__init__()
        self.string = str(string)

class Caracter(Nodo):
    def __init__(self, valor):
        super().__init__()
        self.valor = valor

class Booleano(Nodo):
    def __init__(self, valor):
        super().__init__()
        self.valor = bool(valor)
