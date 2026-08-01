from backend.visitor.grafo import VisitarGrafo

class VisitarStruct(VisitarGrafo):
    def visitar_DeclaracionStruct(self, nodo):
        id_nodo = self._crear_nodo(f'DeclaracionStruct({nodo.nombre_struct})')
        campos = nodo.parametros_struct
        if isinstance(campos, list):
            for p in campos:
                self._enlazador(id_nodo, p)
        else:
            self._enlazador(id_nodo, campos)
        return id_nodo

    def visitar_Parametros(self, nodo):
        return self._crear_nodo(f'Parametros({nodo.parametro}: {nodo.tipo_parametro})')
