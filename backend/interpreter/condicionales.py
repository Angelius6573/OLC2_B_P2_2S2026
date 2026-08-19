from backend.ast_modular.condicionales import Condicional

def visitar_Condicional(self, nodo):
    condicion = self.visitar(nodo.condicion)
    if condicion:
        self._ejecutar_bloque(nodo.bloque_verdadero)
    elif nodo.bloque_falso:
        self._ejecutar_bloque(nodo.bloque_falso)
    return None
