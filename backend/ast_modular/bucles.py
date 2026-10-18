from backend.ast import Nodo

class BloqueBare(Nodo):
    def __init__(self, bloque):
        super().__init__()
        self.bloque = bloque

class BucleWhile(Nodo):
    def __init__(self, condicion, bloque_ambito, label=None):
        super().__init__()
        self.condicion = condicion
        self.bloque_ambito = bloque_ambito
        self.label = label

class BucleLoop(Nodo):
    def __init__(self, bloque_ambito, label=None):
        super().__init__()
        self.bloque_ambito = bloque_ambito
        self.label = label

class BucleFor(Nodo):
    def __init__(self, variable, iterable, bloque_ambito, label=None):
        super().__init__()
        self.variable = variable
        self.iterable = iterable
        self.bloque_ambito = bloque_ambito
        self.label = label

class Rango(Nodo):
    def __init__(self, inicio, fin):
        super().__init__()
        self.inicio = inicio
        self.fin = fin

class Break(Nodo):
    def __init__(self, label=None):
        super().__init__()
        self.label = label

class Continue(Nodo):
    def __init__(self, label=None):
        super().__init__()
        self.label = label
