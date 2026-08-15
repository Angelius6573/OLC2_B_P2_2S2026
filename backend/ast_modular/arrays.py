from backend.ast import Nodo

class AccederIndice(Nodo):
    def __init__(self, objetivo, indices):
        super().__init__()
        self.objetivo = objetivo
        self.indices = indices

class Slice(Nodo):
    def __init__(self, objetivo, inicio, fin):
        super().__init__()
        self.objetivo = objetivo
        self.inicio = inicio
        self.fin = fin

class Repetidor(Nodo):
    def __init__(self, valor, cantidad):
        super().__init__()
        self.valor = valor
        self.cantidad = cantidad

class AsignarIndice(Nodo):
    def __init__(self, objetivo, valor):
        super().__init__()
        self.objetivo = objetivo
        self.valor = valor
