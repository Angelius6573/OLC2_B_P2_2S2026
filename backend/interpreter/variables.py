from backend.ast_modular.variables import DeclaracionVariable, Asignacion, AsignacionCompuesta

def visitar_DeclaracionVariable(self, nodo):
    valor = self.visitar(nodo.valor) if nodo.valor is not None else None
    mutable = nodo.mutabilidad == 'let mut'
    self.ambito_actual.declarar(nodo.nombre, valor, mutable)
    return None

def visitar_Asignacion(self, nodo):
    valor = self.visitar(nodo.valor)
    if not self.ambito_actual.asignar(nodo.nombre, valor):
        raise RuntimeError(f"{nodo.linea}:{nodo.columna} Variable '{nodo.nombre}' no declarada")
    return None

def visitar_AsignacionCompuesta(self, nodo):
    v = self.ambito_actual.buscar(nodo.nombre)
    if v is None:
        raise RuntimeError(f"{nodo.linea}:{nodo.columna} Variable '{nodo.nombre}' no declarada")
    if not v.mutable:
        raise RuntimeError(f"{nodo.linea}:{nodo.columna} Variable '{nodo.nombre}' no es mutable")
    valor = self.visitar(nodo.valor)
    op = nodo.operador[:-1]
    if op == '+':
        v.valor = v.valor + valor
    elif op == '-':
        v.valor = v.valor - valor
    elif op == '*':
        v.valor = v.valor * valor
    elif op == '/':
        v.valor = v.valor / valor
    elif op == '%':
        v.valor = v.valor % valor
    return None
