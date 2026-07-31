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
