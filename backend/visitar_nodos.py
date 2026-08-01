from backend.visitor.funciones import VisitarFunciones
from backend.visitor.impresion import VisitarImpresion
from backend.visitor.aritmetica import VisitarAritmetica
from backend.visitor.struct import VisitarStruct

class VisitarNodos(VisitarFunciones, VisitarImpresion, VisitarAritmetica, VisitarStruct):
    def __init__(self):
        super().__init__()

    def visitar_Programa(self, nodo):
        id_nodo = self._crear_nodo('Programa')
        for e in nodo.declaraciones:
            self._enlazador(id_nodo, e)
        return id_nodo
