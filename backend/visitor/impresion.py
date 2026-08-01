from backend.visitor.grafo import VisitarGrafo

class VisitarImpresion(VisitarGrafo):
    def visitar_Imprimir(self, nodo):
        id_nodo = self._crear_nodo('Imprimir')
        self._enlazador(id_nodo, nodo.argumentos_impresion)
        return id_nodo

    def visitar_ArgumentosImpresion(self, nodo):
        id_nodo = self._crear_nodo(f'ArgumentosImpresion(cadena={nodo.cadena!r})')
        for expr in nodo.operaciones_directas:
            self._enlazador(id_nodo, expr)
        return id_nodo
