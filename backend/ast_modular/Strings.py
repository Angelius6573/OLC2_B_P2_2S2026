from backend.ast import Nodo

class DeclaracionString(Nodo):
    def __init__(self, metodo, valor):
        super().__init__()
        self.metodo = metodo
        self.valor = valor
