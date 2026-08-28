from backend.ast_modular.bucles import (BucleWhile, BucleLoop, BucleFor, Break, Continue, Rango, BloqueBare)
from backend.interpreter.runtime import _BreakSignal, _ContinueSignal

def visitar_BloqueBare(self, nodo):
    self._ejecutar_bloque(nodo.bloque)
    return None

def visitar_BucleWhile(self, nodo):
    while self.visitar(nodo.condicion):
        try:
            self._ejecutar_bloque(nodo.bloque_ambito)
        except _BreakSignal as e:
            if e.label is None or e.label == nodo.label:
                break
            raise
        except _ContinueSignal:
            continue
    return None

def visitar_BucleLoop(self, nodo):
    while True:
        try:
            self._ejecutar_bloque(nodo.bloque_ambito)
        except _BreakSignal as e:
            if e.label is None or e.label == nodo.label:
                break
            raise
        except _ContinueSignal:
            continue
    return None

def visitar_BucleFor(self, nodo):
    iterable = self.visitar(nodo.iterable)
    nombre_var = nodo.variable.id
    if isinstance(iterable, Rango):
        iterable = self.visitar(nodo.iterable)
    if isinstance(iterable, list):
        valores = iterable
    elif isinstance(iterable, range):
        valores = list(iterable)
    else:
        raise RuntimeError(f"{nodo.linea}:{nodo.columna} Iterable no válido")
    for valor in valores:
        self.ambito_actual.declarar(nombre_var, valor)
        try:
            self._ejecutar_bloque(nodo.bloque_ambito)
        except _BreakSignal as e:
            if e.label is None or e.label == nodo.label:
                break
            raise
        except _ContinueSignal:
            continue
    return None

def visitar_Rango(self, nodo):
    inicio = self.visitar(nodo.inicio)
    fin = self.visitar(nodo.fin)
    return range(inicio, fin)

def visitar_Break(self, nodo):
    raise _BreakSignal(nodo.label)

def visitar_Continue(self, nodo):
    raise _ContinueSignal()
