from backend.ast import Nodo

class Imprimir(Nodo):
    def __init__(self, argumentos_impresion):
        super().__init__()
        self.argumentos_impresion = argumentos_impresion

class ArgumentosImpresion(Nodo):
    def __init__(self, cadena, operaciones_directas):
        super().__init__()
        self.cadena = cadena
        self.operaciones_directas = operaciones_directas

