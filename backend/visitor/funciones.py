from backend.visitor.grafo import VisitarGrafo

class VisitarFunciones(VisitarGrafo):
    def visitar_DeclaracionFuncion(self, nodo):
        id_nodo = self._crear_nodo('DeclaracionFuncion')
        self._enlazador(id_nodo, nodo.nombre_funcion)
        self.grafo.edge(id_nodo, self._crear_nodo(f'parametros: {nodo.parametros_funcion}'))
        self.grafo.edge(id_nodo, self._crear_nodo(f'valor_retorno: {nodo.valor_retorno}'))
        for inst in nodo.bloque_ambito:
            self._enlazador(id_nodo, inst)
        return id_nodo

    def visitar_NombreFuncion(self, nodo):
        return self._crear_nodo(f'NombreFuncion({nodo.nombre_conjunto}, {nodo.nombre_funcion})')
