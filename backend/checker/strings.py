from backend.ast_modular.Strings import DeclaracionString
from backend.checker.helpers import se_esperaba

def visitar_DeclaracionString(self, nodo):
    tipo_valor = self.visitar(nodo.valor)
    if nodo.metodo == 'from' and tipo_valor is not None and tipo_valor != 'String':
        se_esperaba(self, nodo, 'String', tipo_valor)
    nodo.tipo = 'String'
    return 'String'
