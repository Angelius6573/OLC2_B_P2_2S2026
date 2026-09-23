from backend.recorrer_ast import RecorrerAST
from backend.checker.tabla_simbolos import TablaSimbolos
from backend.checker.tipos import NUMERICOS, TIPOS_PRIMITIVOS, LITERALES
from backend.checker.helpers import (
    se_esperaba, verificar_asignacion, verificar_tipo_definido,
    es_literal, tipo_elemento, tamano_arreglo, nombre_objetivo, binaria,
)
from backend.checker.declaraciones import (
    visitar_Programa, colectar_declaraciones, _declarar_struct, _declarar_funcion,
    visitar_DeclaracionStruct, visitar_DeclaracionFuncion,
)
from backend.checker.variables import (
    visitar_DeclaracionVariable, visitar_Asignacion, visitar_AsignacionCompuesta,
)
from backend.checker.aritmetica import (
    visitar_OperacionBinaria, visitar_OperacionUnaria, visitar_Variable,
    visitar_NumeroEntero, visitar_NumeroFloat,
    visitar_Cadena, visitar_Caracter, visitar_Booleano,
)
from backend.checker.bucles import (
    visitar_BucleWhile, visitar_BucleLoop, visitar_BucleFor,
    visitar_Break, visitar_Continue, visitar_Rango,
)
from backend.checker.condicionales import visitar_Condicional, visitar_BloqueBare
from backend.checker.funciones import (
    visitar_LlamadaFuncion, visitar_Return, visitar_FuncionEmbebida,
)
from backend.checker.impresion import visitar_Imprimir
from backend.checker.match import visitar_Match, visitar_MatchBase
from backend.checker.struct import visitar_InstanciarStruct, visitar_AccederCampo
from backend.checker.arrays import (
    visitar_AccederIndice, visitar_AsignarIndice, visitar_Slice, visitar_Repetidor,
)
from backend.checker.strings import visitar_DeclaracionString

class AnalizadorSemantico(RecorrerAST):
    def __init__(self):
        self.tabla = TablaSimbolos()
        self.errores = []
        self._en_bucle = 0
        self._funcion_actual = None

    def error(self, linea, columna, mensaje):
        self.errores.append((linea, columna, f"[Semantico] {mensaje}"))

    def tiene_errores(self):
        return bool(self.errores)

    def analizar(self, programa):
        self.colectar_declaraciones(programa)
        self.visitar(programa)
        return self

    def visitar(self, nodo):
        if isinstance(nodo, list):
            pares = []
            for n in nodo:
                tipo = self.visitar(n)
                if tipo is not None:
                    pares.append((n, tipo))
            if not pares:
                return None
            base = pares[0][1]
            for n, tipo in pares[1:]:
                if tipo != base:
                    se_esperaba(self, n, base, tipo)
            return f'[{base}; {len(pares)}]'
        return super().visitar(nodo)

    def _visitar_generico(self, nodo):
        return None

    # Importaciones
    visitar_Programa = visitar_Programa
    colectar_declaraciones = colectar_declaraciones
    _declarar_struct = _declarar_struct
    _declarar_funcion = _declarar_funcion
    visitar_DeclaracionStruct = visitar_DeclaracionStruct
    visitar_DeclaracionFuncion = visitar_DeclaracionFuncion
    visitar_DeclaracionVariable = visitar_DeclaracionVariable
    visitar_Asignacion = visitar_Asignacion
    visitar_AsignacionCompuesta = visitar_AsignacionCompuesta
    visitar_OperacionBinaria = visitar_OperacionBinaria
    visitar_OperacionUnaria = visitar_OperacionUnaria
    visitar_Variable = visitar_Variable
    visitar_NumeroEntero = visitar_NumeroEntero
    visitar_NumeroFloat = visitar_NumeroFloat
    visitar_Cadena = visitar_Cadena
    visitar_Caracter = visitar_Caracter
    visitar_Booleano = visitar_Booleano
    visitar_BucleWhile = visitar_BucleWhile
    visitar_BucleLoop = visitar_BucleLoop
    visitar_BucleFor = visitar_BucleFor
    visitar_Break = visitar_Break
    visitar_Continue = visitar_Continue
    visitar_Rango = visitar_Rango
    visitar_Condicional = visitar_Condicional
    visitar_BloqueBare = visitar_BloqueBare
    visitar_LlamadaFuncion = visitar_LlamadaFuncion
    visitar_Return = visitar_Return
    visitar_FuncionEmbebida = visitar_FuncionEmbebida
    visitar_Imprimir = visitar_Imprimir
    visitar_Match = visitar_Match
    visitar_MatchBase = visitar_MatchBase
    visitar_InstanciarStruct = visitar_InstanciarStruct
    visitar_AccederCampo = visitar_AccederCampo
    visitar_AccederIndice = visitar_AccederIndice
    visitar_AsignarIndice = visitar_AsignarIndice
    visitar_Slice = visitar_Slice
    visitar_Repetidor = visitar_Repetidor
    visitar_DeclaracionString = visitar_DeclaracionString
