from backend.ast_modular.struct import InstanciarStruct, AccederCampo
from backend.checker.helpers import se_esperaba, verificar_asignacion

def visitar_InstanciarStruct(self, nodo):
    struct = self.tabla.buscar_struct(nodo.nombre)
    if struct is None:
        self.error(nodo.linea, nodo.columna, f"El struct '{nodo.nombre}' no está definido")
        return None
    dados = {}
    for parametro in nodo.parametros:
        if parametro.nombre not in struct.campos:
            self.error(parametro.linea, parametro.columna, f"El campo '{parametro.nombre}' no existe en '{nodo.nombre}'")
        tipo_valor = self.visitar(parametro.valor)
        if tipo_valor is not None and parametro.nombre in struct.campos:
            verificar_asignacion(self, parametro, struct.campos[parametro.nombre], tipo_valor)
        dados[parametro.nombre] = True
    faltantes = [campo for campo in struct.campos if campo not in dados]
    if faltantes:
        self.error(nodo.linea, nodo.columna, f"Faltan campos en '{nodo.nombre}': {', '.join(faltantes)}")
    nodo.tipo = nodo.nombre
    return nodo.nombre


def visitar_AccederCampo(self, nodo):
    tipo_objetivo = self.visitar(nodo.objetivo)
    if tipo_objetivo is None:
        return None
    struct = self.tabla.buscar_struct(tipo_objetivo)
    if struct is None:
        se_esperaba(self, nodo, 'struct', tipo_objetivo)
        return None
    if nodo.campo not in struct.campos:
        self.error(nodo.linea, nodo.columna, f"Campo '{nodo.campo}' no existe en '{tipo_objetivo}'")
        return None
    nodo.tipo = struct.campos[nodo.campo]
    return nodo.tipo
