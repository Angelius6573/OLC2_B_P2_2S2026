from backend.ast import Nodo

class Imprimir(Nodo):
    def __init__(self, argumentos_impresion):
        super().__init__()
        self.argumentos_impresion = argumentos_impresion

class ArgumentosImpresion(Nodo):
    def __init__(self, cadena, operaciones_directas, es_rawstring=False):
        super().__init__()
        self.cadena = cadena
        self.operaciones_directas = operaciones_directas
        self.es_rawstring = es_rawstring

