from backend.ast_modular.condicionales import Condicional
from backend.checker.helpers import se_esperaba

def visitar_Condicional(self, nodo):
    tipo_cond = self.visitar(nodo.condicion)

    if tipo_cond is not None and tipo_cond != 'bool':
        se_esperaba(self, nodo, 'bool', tipo_cond)

    self.tabla.abrir_ambito()
    for instruccion in nodo.bloque_verdadero:
        self.visitar(instruccion)
    self.tabla.cerrar_ambito()

    self.tabla.abrir_ambito()
    for instruccion in (nodo.bloque_falso or []):
        self.visitar(instruccion)

    self.tabla.cerrar_ambito()
    return None
