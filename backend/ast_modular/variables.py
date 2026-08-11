from backend.ast import Nodo

class DeclaracionVariable(Nodo):
    def __init__(self, nombre, mutabilidad, tipo, valor):
        super().__init__()
        self.nombre = nombre
        self.mutabilidad = mutabilidad
        self.tipo = tipo
        self.valor = valor
