from backend.ast import Nodo

class DeclaracionFuncion(Nodo):
    def __init__(self, nombre_funcion, parametros_funcion, valor_retorno, bloque_ambito):
        super().__init__()
        self.nombre_funcion = nombre_funcion
        self.parametros_funcion = parametros_funcion
        self.valor_retorno = valor_retorno
        self.bloque_ambito = bloque_ambito

class NombreFuncion(Nodo):
    def __init__(self, nombre_conjunto, nombre_funcion):
        super().__init__()
        self.nombre_conjunto = nombre_conjunto
        self.nombre_funcion = nombre_funcion

class LlamadaFuncion(Nodo):
    def __init__(self, nombre_funcion, parametros):
        super().__init__()
        self.nombre_funcion = nombre_funcion
        self.parametros = parametros
