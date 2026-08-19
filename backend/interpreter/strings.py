from backend.ast_modular.Strings import DeclaracionString

def visitar_DeclaracionString(self, nodo):
    valor = self.visitar(nodo.valor) if nodo.valor else ''
    if nodo.metodo == 'from':
        return str(valor) if valor is not None else ''
    if nodo.metodo == 'new':
        return ''
    return str(valor) if valor is not None else ''
