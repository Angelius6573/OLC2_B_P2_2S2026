"""Intérprete que además recuerda, por sym_id, el último valor de cada variable (columna «Valor»
del reporte de símbolos). La semántica del intérprete no cambia: solo se observa.
Por cada declaración se guarda el objeto Variable que crea el intérprete. Asignar, `+=` y
`push_str` modifican ese mismo objeto, así que al terminar contiene el último valor.
"""
from backend.interpreter.interprete import Interprete
from backend.interpreter.runtime import Variable

class LimitePasos(BaseException):
    # BaseException: no la atrapan los except del intérprete
    pass

class InterpreteConValores(Interprete):
    def __init__(self, tabla, limite_pasos=None):
        super().__init__()
        self.celdas = {}                # sym_id -> Variable del intérprete
        self._limite_pasos = limite_pasos
        self._pasos = 0
        self._parametros = {}           # función -> sym_id de sus parámetros, en orden
        for simbolo in sorted(tabla.variables_por_sym_id.values(), key=lambda s: s.sym_id):
            if simbolo.categoria == 'Parámetro':
                self._parametros.setdefault(simbolo.ambito, []).append(simbolo.sym_id)

    def visitar(self, nodo):
        if self._limite_pasos is not None:
            self._pasos += 1
            if self._pasos > self._limite_pasos:
                raise LimitePasos()
        return super().visitar(nodo)

    def visitar_DeclaracionVariable(self, nodo):
        resultado = super().visitar_DeclaracionVariable(nodo)
        self._recordar(getattr(nodo, 'sym_id', None), nodo.nombre)
        return resultado

    def visitar_BucleFor(self, nodo):
        # La variable del for se declara en el ámbito que contiene al bucle, una vez por vuelta
        nombre = nodo.variable.id
        antes = self.ambito_actual.variables.get(nombre)
        try:
            return super().visitar_BucleFor(nodo)
        finally:
            if self.ambito_actual.variables.get(nombre) is not antes:
                self._recordar(getattr(nodo.variable, 'sym_id', None), nombre)

    def _llamar_funcion(self, nombre, argumentos):
        # Los parámetros no son mutables: su último valor es el argumento de la última llamada
        for sym_id, argumento in zip(self._parametros.get(nombre, []), argumentos):
            self.celdas[sym_id] = Variable(argumento)
        return super()._llamar_funcion(nombre, argumentos)

    def _recordar(self, sym_id, nombre):
        celda = self.ambito_actual.variables.get(nombre)
        if sym_id is not None and celda is not None:
            self.celdas[sym_id] = celda
