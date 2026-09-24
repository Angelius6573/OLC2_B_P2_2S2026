from backend.ast_modular.struct import DeclaracionStruct
from backend.ast_modular.funciones import DeclaracionFuncion
from backend.checker.tabla_simbolos import SimboloFuncion, SimboloStruct, AMBITO_GLOBAL

def colectar_declaraciones(self, programa):
    for declaracion in programa.declaraciones:
        if isinstance(declaracion, DeclaracionStruct):
            _declarar_struct(self, declaracion)
        elif isinstance(declaracion, DeclaracionFuncion):
            _declarar_funcion(self, declaracion)

def _declarar_struct(self, declaracion):
    campos = {}
    for parametro in declaracion.parametros_struct:
        campos[parametro.parametro] = parametro.tipo_parametro
    simbolo = SimboloStruct(
        nombre=declaracion.nombre_struct,
        campos=campos,
        linea=declaracion.linea,
        columna=declaracion.columna,
    )
    if not self.tabla.declarar_struct(simbolo):
        self.error(
            declaracion.linea,
            declaracion.columna, f"El struct '{declaracion.nombre_struct}' ya está definido",
        )

def _declarar_funcion(self, declaracion):
    lista = declaracion.parametros_funcion
    parametros = [(lista[i], lista[i + 1]) for i in range(0, len(lista), 2)]
    retorno = declaracion.valor_retorno if declaracion.valor_retorno else None
    nombre = declaracion.nombre_funcion.nombre_funcion
    simbolo = SimboloFuncion(
        nombre=nombre,
        parametros=parametros,
        retorno=retorno,
        linea=declaracion.linea,
        columna=declaracion.columna,
    )
    if not self.tabla.declarar_funcion(simbolo):
        self.error(
            declaracion.linea,
            declaracion.columna, f"La función '{nombre}' ya está definida",
        )

def visitar_Programa(self, nodo):
    for declaracion in nodo.declaraciones:
        self.visitar(declaracion)
    return None

def visitar_DeclaracionStruct(self, nodo):
    return None

def visitar_DeclaracionFuncion(self, nodo):
    from backend.checker.tabla_simbolos import SimboloVariable
    nombre = nodo.nombre_funcion.nombre_funcion
    simbolo = self.tabla.buscar_funcion(nombre)
    if simbolo is None:
        return None
    self.tabla.abrir_ambito()
    self.tabla.ambito_nombre = nombre
    # La gramática no guarda la posición de cada parámetro: llevan la de la función
    for nombre_param, tipo_param in simbolo.parametros:
        if not self.tabla.declarar_variable(SimboloVariable(
            nombre=nombre_param,
            tipo=tipo_param,
            mutable=False,
            linea=simbolo.linea,
            columna=simbolo.columna,
            categoria='Parámetro',
        )):
            self.error(nodo.linea, nodo.columna, f"La variable '{nombre_param}' ya está definida")
    self._funcion_actual = simbolo
    for instruccion in nodo.bloque_ambito:
        self.visitar(instruccion)
    self._funcion_actual = None
    self.tabla.ambito_nombre = AMBITO_GLOBAL
    self.tabla.cerrar_ambito()
    return None
