from backend.ast_modular.condicionales import Condicional
from backend.ast_modular.bucles import BloqueBare
from backend.checker.helpers import se_esperaba

def visitar_Condicional(self, nodo):
    tipo_cond = self.visitar(nodo.condicion)

    if tipo_cond is not None and tipo_cond != 'bool':
        se_esperaba(self, nodo, 'bool', tipo_cond)

    self.tabla.abrir_ambito()
    for instruccion in nodo.bloque_verdadero:
        self.visitar(instruccion)
    self.tabla.cerrar_ambito()

    if nodo.bloque_falso:
        self.tabla.abrir_ambito()
        if isinstance(nodo.bloque_falso, list):
            for instruccion in nodo.bloque_falso:
                self.visitar(instruccion)
        else:
            self.visitar(nodo.bloque_falso)
        self.tabla.cerrar_ambito()
    return None

def visitar_BloqueBare(self, nodo):
    self.tabla.abrir_ambito()
    for instruccion in nodo.bloque:
        self.visitar(instruccion)
    self.tabla.cerrar_ambito()
    return None
