from backend.ast_modular.match import Match, MatchBase

def visitar_Match(self, nodo):
    valor = self.visitar(nodo.expresion)
    for brazo in nodo.brazos:
        if isinstance(brazo.patron, MatchBase):
            return self.visitar(brazo.cuerpo)
        patron_val = self.visitar(brazo.patron)
        if valor == patron_val:
            return self.visitar(brazo.cuerpo)
    return None

def visitar_MatchBase(self, nodo):
    return None
