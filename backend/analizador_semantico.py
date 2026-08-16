from backend.ast_modular.funciones import DeclaracionFuncion
from backend.ast_modular.struct import DeclaracionStruct
from backend.checker.tabla_simbolos import TablaSimbolos, SimboloFuncion, SimboloStruct

class AnalizadorSemantico:
    def __init__(self):
        self.tabla = TablaSimbolos()
        self.errores = []

    def error(self, linea, columna, mensaje):
        self.errores.append((linea, columna, mensaje))

    def tiene_errores(self):
        return bool(self.errores)

    def analizar(self, programa):
        self.colectar_declaraciones(programa)
        return self

    def colectar_declaraciones(self, programa):
        for declaracion in programa.declaraciones:
            if isinstance(declaracion, DeclaracionStruct):
                self._declarar_struct(declaracion)
            elif isinstance(declaracion, DeclaracionFuncion):
                self._declarar_funcion(declaracion)

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
                declaracion.columna,
                f"El struct '{declaracion.nombre_struct}' ya está definido",
            )

    def _declarar_funcion(self, declaracion):
        lista = declaracion.parametros_funcion
        parametros = [
            (lista[i], lista[i + 1])
            for i in range(0, len(lista), 2)
        ]
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
                declaracion.columna,
                f"La función '{nombre}' ya está definida",
            )
