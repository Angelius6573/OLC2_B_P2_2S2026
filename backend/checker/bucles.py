from backend.ast_modular.bucles import BucleWhile, BucleLoop, BucleFor, Break, Continue, Rango
from backend.checker.tabla_simbolos import SimboloVariable
from backend.checker.helpers import se_esperaba, tipo_elemento

def visitar_BucleWhile(self, nodo):
    tipo_cond = self.visitar(nodo.condicion)
    if tipo_cond is not None and tipo_cond != 'bool':
        se_esperaba(self, nodo, 'bool', tipo_cond)
    self.tabla.abrir_ambito()
    self._en_bucle += 1
    for instruccion in nodo.bloque_ambito:
        self.visitar(instruccion)
    self._en_bucle -= 1
    self.tabla.cerrar_ambito()
    return None

def visitar_BucleLoop(self, nodo):
    self.tabla.abrir_ambito()
    self._en_bucle += 1
    for instruccion in nodo.bloque_ambito:
        self.visitar(instruccion)
    self._en_bucle -= 1
    self.tabla.cerrar_ambito()
    return None

def visitar_BucleFor(self, nodo):
    if isinstance(nodo.iterable, Rango):
        self.visitar(nodo.iterable)
        tipo_variable = 'i32'
    else:
        tipo_iter = self.visitar(nodo.iterable)
        if tipo_iter is not None and tipo_iter.startswith('['):
            tipo_variable = tipo_elemento(tipo_iter)
        else:
            tipo_variable = None
            if tipo_iter is not None:
                se_esperaba(self, nodo, 'rango o arreglo', tipo_iter)
    self.tabla.abrir_ambito()
    simbolo = SimboloVariable(
        nombre=nodo.variable.id,
        tipo=tipo_variable,
        mutable=False,
        linea=nodo.variable.linea,
        columna=nodo.variable.columna,
    )
    self.tabla.declarar_variable(simbolo)
    nodo.variable.sym_id = simbolo.sym_id
    self._en_bucle += 1
    for instruccion in nodo.bloque_ambito:
        self.visitar(instruccion)
    self._en_bucle -= 1
    self.tabla.cerrar_ambito()
    return None

def visitar_Rango(self, nodo):
    for extremo in (nodo.inicio, nodo.fin):
        tipo = self.visitar(extremo)
        if tipo is not None and tipo != 'i32':
            se_esperaba(self, extremo, 'i32', tipo)
    nodo.tipo = 'i32'
    return 'i32'

def visitar_Break(self, nodo):
    if self._en_bucle == 0:
        self.error(nodo.linea, nodo.columna, "La sentencia break está fuera de un bucle.")
    return None

def visitar_Continue(self, nodo):
    if self._en_bucle == 0:
        self.error(nodo.linea, nodo.columna, "La sentencia continue está fuera de un bucle.")
    return None
