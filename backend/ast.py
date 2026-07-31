class Nodo:
    def __init__(self, linea=None, columna=None):
        self.linea = linea
        self.columna = columna

    def __repr__(self):
        return f"{self.__class__.__name__}(...)"

# Programa
class Programa(Nodo):
    def __init__(self, declaraciones):
        super().__init__()
        self.declaraciones = declaraciones

# Funciones
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
