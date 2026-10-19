from backend.ast_modular.arrays import AccederIndice, AsignarIndice, Slice, Repetidor
from backend.ast_modular.aritmetica import NumeroEntero
from backend.checker.helpers import se_esperaba, verificar_asignacion, tipo_elemento, tamano_arreglo

def visitar_AccederIndice(self, nodo):
    tipo_objetivo = self.visitar(nodo.objetivo)
    tipo_actual = tipo_objetivo
    for indice in nodo.indices:
        tipo_indice = self.visitar(indice)
        if tipo_indice is not None and tipo_indice != 'i32':
            se_esperaba(self, indice, 'i32', tipo_indice)
        if tipo_actual is None:
            continue
        if not tipo_actual.startswith('['):
            se_esperaba(self, nodo, 'arreglo', tipo_actual)
            return None
        if isinstance(indice, NumeroEntero):
            tamano = tamano_arreglo(tipo_actual)
            if tamano is not None and not (0 <= indice.valor < tamano):
                self.error(nodo.linea, nodo.columna, "Índice fuera de los límites del arreglo.")
        tipo_actual = tipo_elemento(tipo_actual)
    nodo.tipo = tipo_actual
    return tipo_actual

def visitar_AsignarIndice(self, nodo):
    tipo_elemento_val = self.visitar(nodo.objetivo)
    tipo_valor = self.visitar(nodo.valor)
    if tipo_elemento_val is None or tipo_valor is None:
        return None
    if tipo_elemento_val != tipo_valor:
        verificar_asignacion(self, nodo, tipo_elemento_val, tipo_valor)
    return None

def visitar_Slice(self, nodo):
    tipo_objetivo = self.visitar(nodo.objetivo)
    for extremo in (nodo.inicio, nodo.fin):
        tipo_extremo = self.visitar(extremo)
        if tipo_extremo is not None and tipo_extremo != 'i32':
            se_esperaba(self, extremo, 'i32', tipo_extremo)
    if tipo_objetivo is None:
        return None
    if not tipo_objetivo.startswith('['):
        se_esperaba(self, nodo, 'arreglo', tipo_objetivo)
        return None
    nodo.tipo = '&[' + tipo_elemento(tipo_objetivo) + ']'
    return nodo.tipo

def visitar_Repetidor(self, nodo):
    tipo_valor = self.visitar(nodo.valor)
    tipo_cantidad = self.visitar(nodo.cantidad)
    if tipo_cantidad is not None and tipo_cantidad != 'i32':
        se_esperaba(self, nodo.cantidad, 'i32', tipo_cantidad)
    if tipo_valor is None:
        return None
    if isinstance(nodo.cantidad, NumeroEntero):
        nodo.tipo = f'[{tipo_valor}; {nodo.cantidad.valor}]'
    else:
        nodo.tipo = f'[{tipo_valor}; n]'
    return nodo.tipo
