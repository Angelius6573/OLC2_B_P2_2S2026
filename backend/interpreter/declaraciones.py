from backend.ast_modular.struct import DeclaracionStruct
from backend.ast_modular.funciones import DeclaracionFuncion
from backend.interpreter.runtime import Funcion, StructDef

def visitar_Programa(self, nodo):
    for declaracion in nodo.declaraciones:
        self.visitar(declaracion)
    main = self.funciones.get('main')
    if main is not None:
        self._llamar_funcion('main', [])
    return None

def visitar_DeclaracionStruct(self, nodo):
    campos = {}
    for param in nodo.parametros_struct:
        campos[param.parametro] = param.tipo_parametro
    self.structs[nodo.nombre_struct] = StructDef(campos)
    return None

def visitar_DeclaracionFuncion(self, nodo):
    nombre = nodo.nombre_funcion.nombre_funcion
    flat = nodo.parametros_funcion
    parametros = [(flat[i], flat[i + 1]) for i in range(0, len(flat), 2)]
    bloque = nodo.bloque_ambito
    retorno = nodo.valor_retorno
    self.funciones[nombre] = Funcion(parametros, bloque, retorno)
    return None
