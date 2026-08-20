from backend.ast_modular.struct import InstanciarStruct, AccederCampo
from backend.interpreter.runtime import InstanciaStruct

def visitar_InstanciarStruct(self, nodo):
    campos = {}
    for param in nodo.parametros:
        campos[param.nombre] = self.visitar(param.valor)
    return InstanciaStruct(campos)

def visitar_AccederCampo(self, nodo):
    objetivo = self.visitar(nodo.objetivo)
    if isinstance(objetivo, InstanciaStruct):
        if nodo.campo in objetivo.campos:
            return objetivo.campos[nodo.campo]
        raise RuntimeError(f"{nodo.linea}:{nodo.columna} Campo '{nodo.campo}' no existe")
    raise RuntimeError(f"{nodo.linea}:{nodo.columna} No se puede acceder al campo solicitado")
