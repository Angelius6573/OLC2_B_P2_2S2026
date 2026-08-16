from backend.ast import Nodo

class Match(Nodo):
    def __init__(self, expresion, brazos):
        super().__init__()
        self.expresion = expresion
        self.brazos = brazos

class MatchCase(Nodo):
    def __init__(self, patron, cuerpo):
        super().__init__()
        self.patron = patron
        self.cuerpo = cuerpo

class MatchBase(Nodo):
    def __init__(self):
        super().__init__()
