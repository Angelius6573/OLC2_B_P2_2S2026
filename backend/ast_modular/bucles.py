from backend.ast import Nodo

class BucleWhile(Nodo):
    def __init__(self, condicion, bloque_ambito):
        super().__init__()
        self.condicion = condicion
        self.bloque_ambito = bloque_ambito

class BucleLoop(Nodo):
    def __init__(self, bloque_ambito):
        super().__init__()
        self.bloque_ambito = bloque_ambito

class BucleFor(Nodo):
    def __init__(self, variable, iterable, bloque_ambito):
        super().__init__()
        self.variable = variable
        self.iterable = iterable
        self.bloque_ambito = bloque_ambito

class Rango(Nodo):
    def __init__(self, inicio, fin):
        super().__init__()
        self.inicio = inicio
        self.fin = fin

class Break(Nodo):
    def __init__(self):
        super().__init__()

class Continue(Nodo):
    def __init__(self):
        super().__init__()
