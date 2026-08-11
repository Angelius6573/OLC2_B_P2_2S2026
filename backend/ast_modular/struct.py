from backend.ast import Nodo

class DeclaracionStruct(Nodo):
    def __init__(self, nombre_struct, parametros_struct):
        super().__init__()
        self.nombre_struct = nombre_struct
        self.parametros_struct = parametros_struct

class Parametros(Nodo):
    def __init__(self, parametro, tipo_parametro):
        super().__init__()
        self.parametro = parametro
        self.tipo_parametro = tipo_parametro

class ValorRequerido(Nodo):
    def __init__(self, valor):
        super().__init__()
        self.valor = valor

class InstanciarStruct(Nodo):
    def __init__(self, nombre, parametros):
        super().__init__()
        self.nombre = nombre
        self.parametros = parametros

class AsignarParametro(Nodo):
    def __init__(self, nombre, valor):
        super().__init__()
        self.nombre = nombre
        self.valor = valor

class AccederCampo(Nodo):
    def __init__(self, objetivo, campo):
        super().__init__()
        self.objetivo = objetivo
        self.campo = campo
