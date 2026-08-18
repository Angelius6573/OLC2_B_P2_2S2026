from backend.ast_modular.match import Match, MatchBase
from backend.checker.helpers import se_esperaba

def visitar_Match(self, nodo):
    tipo_expr = self.visitar(nodo.expresion)
    if not nodo.brazos:
        self.error(nodo.linea, nodo.columna, "match sin brazos")
    tipo_cuerpo = None
    hay_cuerpo = False
    for brazo in nodo.brazos:
        if not isinstance(brazo.patron, MatchBase):
            tipo_patron = self.visitar(brazo.patron)
            if tipo_expr is not None and tipo_patron is not None and tipo_patron != tipo_expr:
                self.error(brazo.patron.linea, brazo.patron.columna, f"Patrón de tipo '{tipo_patron}' incompatible con '{tipo_expr}'")
        tipo_brazo = self.visitar(brazo.cuerpo)
        if tipo_brazo is not None:
            if not hay_cuerpo:
                tipo_cuerpo = tipo_brazo
                hay_cuerpo = True
            elif tipo_brazo != tipo_cuerpo:
                se_esperaba(self, brazo.cuerpo, tipo_cuerpo, tipo_brazo)
    nodo.tipo = tipo_cuerpo if hay_cuerpo else tipo_expr
    return nodo.tipo

def visitar_MatchBase(self, nodo):
    return None
