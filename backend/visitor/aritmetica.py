from backend.visitor.grafo import VisitarGrafo

class VisitarAritmetica(VisitarGrafo):
    def visitar_OperacionBinaria(self, nodo):
        id_nodo = self._crear_nodo(f'OperacionBinaria({nodo.operador})')
        self._enlazador(id_nodo, nodo.izquierda)
        self._enlazador(id_nodo, nodo.derecha)
        return id_nodo

    def visitar_OperacionUnaria(self, nodo):
        id_nodo = self._crear_nodo(f'OperacionUnaria({nodo.operador})')
        self._enlazador(id_nodo, nodo.derecha)
        return id_nodo

    def visitar_Variable(self, nodo):
        return self._crear_nodo(f'Variable({nodo.id})')

    def visitar_NumeroEntero(self, nodo):
        return self._crear_nodo(f'NumeroEntero({nodo.valor})')

    def visitar_NumeroFloat(self, nodo):
        return self._crear_nodo(f'NumeroFloat({nodo.valor})')
