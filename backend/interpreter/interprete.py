import sys
from backend.recorrer_ast import RecorrerAST
from backend.interpreter.runtime import (
    _ReturnValue, _BreakSignal, _ContinueSignal,
    Variable, Funcion, StructDef, InstanciaStruct, Ambito,
)

from backend.interpreter.expressions import (
    visitar_NumeroEntero, visitar_NumeroFloat,
    visitar_Cadena, visitar_Caracter, visitar_Booleano,
    visitar_OperacionBinaria, visitar_OperacionUnaria,
    visitar_Variable,
)
from backend.interpreter.variables import (
    visitar_DeclaracionVariable, visitar_Asignacion, visitar_AsignacionCompuesta,
)
from backend.interpreter.declaraciones import (
    visitar_Programa, visitar_DeclaracionStruct, visitar_DeclaracionFuncion,
)
from backend.interpreter.condicionales import visitar_Condicional
from backend.interpreter.bucles import (
    visitar_BucleWhile, visitar_BucleLoop, visitar_BucleFor,
    visitar_Rango, visitar_Break, visitar_Continue,
    visitar_BloqueBare,
)
from backend.interpreter.funciones import (
    visitar_LlamadaFuncion, visitar_Return, visitar_FuncionEmbebida,
    _llamar_funcion,
)
from backend.interpreter.impresion import visitar_Imprimir
from backend.interpreter.arrays import (
    visitar_AccederIndice, visitar_AsignarIndice, visitar_Slice, visitar_Repetidor,
)
from backend.interpreter.struct_interpreter import (
    visitar_InstanciarStruct, visitar_AccederCampo,
)
from backend.interpreter.match import visitar_Match, visitar_MatchBase
from backend.interpreter.strings import visitar_DeclaracionString


def _typeof(args):
    val = args[0] if args else None
    if val is None:
        return 'null'
    if isinstance(val, bool):
        return 'bool'
    if isinstance(val, int):
        return 'i32'
    if isinstance(val, float):
        return 'f64'
    if isinstance(val, str):
        return 'String'
    if isinstance(val, list):
        return 'Array'
    if isinstance(val, InstanciaStruct):
        return 'Struct'
    return 'unknown'

def _random(args):
    import random
    if len(args) == 2:
        return random.randint(args[0], args[1])
    if len(args) == 1:
        return random.randint(0, args[0])
    return random.randint(0, 100)

def _len(args, objetivo=None):
    obj = objetivo if objetivo is not None else (args[0] if args else None)
    if isinstance(obj, str):
        return len(obj)
    if isinstance(obj, list):
        return len(obj)
    return 0

def _push_str(args, objetivo=None):
    obj = objetivo if objetivo is not None else None
    if isinstance(obj, str) and args:
        return obj + str(args[0])
    return obj

def _to_uppercase(args, objetivo=None):
    obj = objetivo if objetivo is not None else None
    return obj.upper() if isinstance(obj, str) else obj

def _to_lowercase(args, objetivo=None):
    obj = objetivo if objetivo is not None else None
    return obj.lower() if isinstance(obj, str) else obj

def _reverse(args, objetivo=None):
    obj = objetivo if objetivo is not None else None
    return obj[::-1] if isinstance(obj, str) else obj

def _replace(args, objetivo=None):
    obj = objetivo if objetivo is not None else None
    if isinstance(obj, str) and len(args) >= 2:
        return obj.replace(str(args[0]), str(args[1]))
    return obj

def _contains(args, objetivo=None):
    obj = objetivo if objetivo is not None else None
    return str(args[0]) in obj if isinstance(obj, str) and args else False

def _split(args, objetivo=None):
    obj = objetivo if objetivo is not None else None
    return obj.split(str(args[0])) if isinstance(obj, str) and args else ([obj] if obj is not None else [])

class Interprete(RecorrerAST):
    def __init__(self):
        self.ambito_global = Ambito()
        self.ambito_actual = self.ambito_global
        self.funciones = {}
        self.structs = {}
        self._funciones_embebidas = {
            'typeof': _typeof,
            'random': _random,
            'len': lambda args: _len(args),
            'push_str': lambda args: _push_str(args),
            'to_uppercase': lambda args: _to_uppercase(args),
            'to_lowercase': lambda args: _to_lowercase(args),
            'reverse': lambda args: _reverse(args),
            'replace': lambda args: _replace(args),
            'contains': lambda args: _contains(args),
            'split': lambda args: _split(args),
        }

    def _ejecutar_bloque(self, bloque):
        anterior = self.ambito_actual
        self.ambito_actual = Ambito(anterior)
        try:
            for instruccion in bloque:
                self.visitar(instruccion)
        finally:
            self.ambito_actual = anterior

    def _visitar_generico(self, nodo):
        return None

    def visitar(self, nodo):
        if isinstance(nodo, list):
            return [self.visitar(item) for item in nodo]
        return super().visitar(nodo)

    def ejecutar(self, programa):
        try:
            self.visitar(programa)
        except RuntimeError as e:
            from backend.errores import reportar
            msg = str(e)
            reportar('Ejecucion', 0, 0, msg)
            print(f"[Ejecucion] {msg}", file=sys.stderr)
            sys.exit(1)

    visitar_Programa = visitar_Programa
    visitar_DeclaracionStruct = visitar_DeclaracionStruct
    visitar_DeclaracionFuncion = visitar_DeclaracionFuncion
    visitar_NumeroEntero = visitar_NumeroEntero
    visitar_NumeroFloat = visitar_NumeroFloat
    visitar_Cadena = visitar_Cadena
    visitar_Caracter = visitar_Caracter
    visitar_Booleano = visitar_Booleano
    visitar_OperacionBinaria = visitar_OperacionBinaria
    visitar_OperacionUnaria = visitar_OperacionUnaria
    visitar_Variable = visitar_Variable
    visitar_DeclaracionVariable = visitar_DeclaracionVariable
    visitar_Asignacion = visitar_Asignacion
    visitar_AsignacionCompuesta = visitar_AsignacionCompuesta
    visitar_Condicional = visitar_Condicional
    visitar_BucleWhile = visitar_BucleWhile
    visitar_BucleLoop = visitar_BucleLoop
    visitar_BucleFor = visitar_BucleFor
    visitar_Rango = visitar_Rango
    visitar_Break = visitar_Break
    visitar_Continue = visitar_Continue
    visitar_BloqueBare = visitar_BloqueBare
    visitar_LlamadaFuncion = visitar_LlamadaFuncion
    visitar_Return = visitar_Return
    visitar_FuncionEmbebida = visitar_FuncionEmbebida
    _llamar_funcion = _llamar_funcion
    visitar_Imprimir = visitar_Imprimir
    visitar_AccederIndice = visitar_AccederIndice
    visitar_AsignarIndice = visitar_AsignarIndice
    visitar_Slice = visitar_Slice
    visitar_Repetidor = visitar_Repetidor
    visitar_InstanciarStruct = visitar_InstanciarStruct
    visitar_AccederCampo = visitar_AccederCampo
    visitar_Match = visitar_Match
    visitar_MatchBase = visitar_MatchBase
    visitar_DeclaracionString = visitar_DeclaracionString
