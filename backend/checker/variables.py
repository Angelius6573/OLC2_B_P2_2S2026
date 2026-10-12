from backend.ast_modular.variables import DeclaracionVariable, Asignacion, AsignacionCompuesta
from backend.checker.tabla_simbolos import SimboloVariable
from backend.checker.helpers import (
    se_esperaba, verificar_asignacion, verificar_tipo_definido, binaria,
    operador_invalido, no_declarada, inmutable,
)

def visitar_DeclaracionVariable(self, nodo):
    tipo_valor = self.visitar(nodo.valor) if nodo.valor is not None else None
    tipo = nodo.tipo
    if tipo is None:
        tipo = tipo_valor
    else:
        verificar_tipo_definido(self, tipo, nodo)
        if tipo_valor is not None:
            verificar_asignacion(self, nodo, tipo, tipo_valor)
    nodo.tipo = tipo
    simbolo = SimboloVariable(
        nombre=nodo.nombre,
        tipo=tipo,
        mutable=nodo.mutabilidad == 'let mut',
        linea=nodo.linea,
        columna=nodo.columna,
    )
    if not self.tabla.declarar_variable(simbolo):
        self.error(nodo.linea, nodo.columna, f"La variable '{nodo.nombre}' ya fue declarada en este ámbito.")
    nodo.sym_id = simbolo.sym_id
    return None

def visitar_Asignacion(self, nodo):
    simbolo = self.tabla.buscar_variable(nodo.nombre)
    if simbolo is None:
        no_declarada(self, nodo, nodo.nombre)
        return None
    nodo.sym_id = simbolo.sym_id
    if not simbolo.mutable:
        inmutable(self, nodo, nodo.nombre)
    tipo_valor = self.visitar(nodo.valor)
    if tipo_valor is not None and simbolo.tipo is not None:
        verificar_asignacion(self, nodo, simbolo.tipo, tipo_valor)
    return None

def visitar_AsignacionCompuesta(self, nodo):
    simbolo = self.tabla.buscar_variable(nodo.nombre)
    if simbolo is None:
        no_declarada(self, nodo, nodo.nombre)
        return None
    nodo.sym_id = simbolo.sym_id
    if not simbolo.mutable:
        inmutable(self, nodo, nodo.nombre)
    tipo_valor = self.visitar(nodo.valor)
    if tipo_valor is None or simbolo.tipo is None:
        return None
    op = nodo.operador[:-1]
    resultado = binaria(op, simbolo.tipo, tipo_valor)
    if resultado is None:
        operador_invalido(self, nodo, nodo.operador, simbolo.tipo, tipo_valor)
    elif resultado != simbolo.tipo:
        se_esperaba(self, nodo, simbolo.tipo, resultado)
    return None
