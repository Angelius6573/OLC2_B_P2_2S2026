from backend.ast import Nodo

class Condicional(Nodo):
    def __init__(self, condicion, bloque_verdadero, bloque_falso):
        super().__init__()
        self.condicion = condicion
        self.bloque_verdadero = bloque_verdadero
        self.bloque_falso = bloque_falso
