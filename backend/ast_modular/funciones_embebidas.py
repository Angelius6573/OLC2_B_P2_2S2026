from backend.ast import Nodo

class FuncionEmbebida(Nodo):
    def __init__(self, nombre, objetivo=None, argumentos=None):
        super().__init__()
        self.nombre = nombre
        self.objetivo = objetivo
        self.argumentos = argumentos or []
