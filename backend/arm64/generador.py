from backend.recorrer_ast import RecorrerAST
from backend.arm64.errores import ErrorGeneracion, emitir_error_runtime
from backend.arm64.layout import LIMITE_OFFSET_LDP, LIMITE_SUB_INMEDIATO
from backend.arm64.programa import ProgramaARM64
from backend.arm64.generacion import tipos
from backend.arm64.generacion.tipos import posicion
from backend.arm64.generacion.constantes import (
    visitar_NumeroEntero, visitar_NumeroFloat, visitar_Cadena, visitar_Caracter, visitar_Booleano,
)
from backend.arm64.generacion.variables import (
    visitar_Variable, visitar_DeclaracionVariable, visitar_Asignacion, visitar_AsignacionCompuesta,
    valor_por_defecto,
)
from backend.arm64.generacion.aritmetica import (
    visitar_OperacionBinaria, visitar_OperacionUnaria, operar_binaria,
)
from backend.arm64.generacion.control import (
    visitar_Condicional, visitar_BloqueBare, visitar_BucleWhile, visitar_BucleLoop,
    visitar_BucleFor, visitar_Break, visitar_Continue,
)
from backend.arm64.generacion.funciones import (
    visitar_Programa, visitar_DeclaracionFuncion, visitar_LlamadaFuncion, visitar_Return,
)
from backend.arm64.generacion.impresion import visitar_Imprimir
from backend.arm64.generacion.match import visitar_Match
from backend.arm64.generacion.arreglos import (
    arreglo_literal, visitar_AccederIndice, visitar_AsignarIndice, visitar_Repetidor,
    direccion_elemento, guardar_en_direccion,
)
from backend.arm64.generacion.strings import visitar_DeclaracionString, visitar_FuncionEmbebida

_STRUCTS = 'los structs son opcionales (PLAN F7) y se ejecutan en modo intérprete'
NO_SOPORTADOS = {
    'InstanciarStruct': _STRUCTS,
    'AccederCampo': _STRUCTS,
    'Slice': 'los slices son opcionales (PLAN F8) y se ejecutan en modo intérprete',
}

class GeneradorARM64(RecorrerAST):
    """Recorre el AST ya validado por el checker y arma programa.s.

    Contrato de una expresión: deja su valor en x0, y en x1 la segunda palabra si es String o
    arreglo (puntero y longitud). Una sentencia es una expresión cuyo valor se descarta. Los
    valores intermedios viven en temporales del marco, nunca en la pila con push.
    """
    def __init__(self, tabla):
        self.tabla = tabla
        self.programa = ProgramaARM64()
        self.marco = None
        self.funcion = None
        self.e = None
        self._contador = 0
        self._bucles = []           # (etiqueta del usuario, destino de continue, destino de break)
        self._fin_sentencia = None
        self._descriptores = set()

    def generar(self, programa):
        self.visitar(programa)
        return self.programa.texto()

    def visitar(self, nodo):
        # Una lista en posición de expresión es un literal de arreglo
        if isinstance(nodo, list):
            return self.arreglo_literal(nodo, self.tipo_de(nodo))
        return super().visitar(nodo)

    def _visitar_generico(self, nodo):
        # Nunca se emite código vacío por un nodo no implementado (PLAN §3.5)
        nombre = type(nodo).__name__
        motivo = NO_SOPORTADOS.get(nombre, 'no tiene generación de código')
        raise ErrorGeneracion(f'{nombre} no se puede compilar a ARM64: {motivo}', *posicion(nodo))

    # Etiquetas y sentencias

    def nuevo_numero(self):
        self._contador += 1
        return self._contador

    def bloque(self, sentencias):
        for sentencia in sentencias or []:
            self.sentencia(sentencia)

    def sentencia(self, nodo):
        """Visita una sentencia. Si una expresión suya falla en runtime, salta a su final."""
        if nodo is None:
            return
        anterior = self._fin_sentencia
        self._fin_sentencia = None
        self.visitar(nodo)
        if self._fin_sentencia is not None:
            self.e.etiqueta(self._fin_sentencia)
        self._fin_sentencia = anterior

    def error_runtime(self, codigo, nodo):
        # mov x6 + bl ox_error + salto al final de la sentencia (PLAN §2.10)
        if self._fin_sentencia is None:
            self._fin_sentencia = f'fin_sentencia_{self.nuevo_numero()}'
        linea, columna = posicion(nodo)
        emitir_error_runtime(self.e, codigo, linea, columna)
        self.e.instr('b', self._fin_sentencia)

    # Tipos

    def tipo_de(self, nodo):
        if isinstance(nodo, list):
            if not nodo:
                return None
            interior = self.tipo_de(nodo[0])
            return f'[{interior}; {len(nodo)}]' if interior is not None else None
        return getattr(nodo, 'tipo', None)

    def tipo(self, nodo):
        tipo = self.tipo_de(nodo)
        if tipo is None:
            raise ErrorGeneracion('La expresión no tiene tipo; no se puede compilar a ARM64',
                                  *posicion(nodo))
        return tipo

    def simbolo(self, sym_id):
        return self.tabla.variables_por_sym_id[sym_id]

    # Slots del marco y temporales

    def temporal(self):
        return self.marco.reservar_temporal()

    def cargar_slot(self, offset, par, r0='x0', r1='x1', comentario=None):
        if not par:
            self.e.instr('ldr', r0, f'[x29, #{offset}]', comentario=comentario)
        elif offset <= LIMITE_OFFSET_LDP:
            self.e.instr('ldp', r0, r1, f'[x29, #{offset}]', comentario=comentario)
        else:
            self.e.instr('ldr', r0, f'[x29, #{offset}]', comentario=comentario)
            self.e.instr('ldr', r1, f'[x29, #{offset + 8}]')

    def guardar_slot(self, offset, par, r0='x0', r1='x1', comentario=None):
        if not par:
            self.e.instr('str', r0, f'[x29, #{offset}]', comentario=comentario)
        elif offset <= LIMITE_OFFSET_LDP:
            self.e.instr('stp', r0, r1, f'[x29, #{offset}]', comentario=comentario)
        else:
            self.e.instr('str', r0, f'[x29, #{offset}]', comentario=comentario)
            self.e.instr('str', r1, f'[x29, #{offset + 8}]')

    def sumar_inmediato(self, destino, origen, valor):
        if valor == 0:
            if destino != origen:
                self.e.instr('mov', destino, origen)
        elif valor <= LIMITE_SUB_INMEDIATO:
            self.e.instr('add', destino, origen, f'#{valor}')
        else:
            self.e.cargar_inmediato('x15', valor)
            self.e.instr('add', destino, origen, 'x15')

    def cargar_texto(self, contenido):
        etiqueta = self.programa.literales.etiqueta(contenido)
        self.e.instr('ldr', 'x0', f'={etiqueta}')
        self.e.instr('mov', 'x1', self.programa.literales.longitud(etiqueta))

    def descriptor(self, tipo):
        """Registra en .rodata el descriptor de ox_print_array de este arreglo y da su etiqueta."""
        nombre = tipos.nombre_descriptor(tipo)
        if nombre not in self._descriptores:
            self._descriptores.add(nombre)
            self.programa.datos.etiqueta(nombre)
            self.programa.datos.directiva('.quad ' + ', '.join(tipos.descriptor(tipo)))
        return nombre

    # Bloque 1: literales
    visitar_NumeroEntero = visitar_NumeroEntero
    visitar_NumeroFloat = visitar_NumeroFloat
    visitar_Cadena = visitar_Cadena
    visitar_Caracter = visitar_Caracter
    visitar_Booleano = visitar_Booleano
    # Bloque 2: variables
    visitar_Variable = visitar_Variable
    visitar_DeclaracionVariable = visitar_DeclaracionVariable
    visitar_Asignacion = visitar_Asignacion
    visitar_AsignacionCompuesta = visitar_AsignacionCompuesta
    valor_por_defecto = valor_por_defecto
    # Bloque 3: aritmética
    visitar_OperacionBinaria = visitar_OperacionBinaria
    visitar_OperacionUnaria = visitar_OperacionUnaria
    operar_binaria = operar_binaria
    # Bloque 4: control de flujo
    visitar_Condicional = visitar_Condicional
    visitar_BloqueBare = visitar_BloqueBare
    visitar_BucleWhile = visitar_BucleWhile
    visitar_BucleLoop = visitar_BucleLoop
    visitar_BucleFor = visitar_BucleFor
    visitar_Break = visitar_Break
    visitar_Continue = visitar_Continue
    # Bloque 5: funciones
    visitar_Programa = visitar_Programa
    visitar_DeclaracionFuncion = visitar_DeclaracionFuncion
    visitar_LlamadaFuncion = visitar_LlamadaFuncion
    visitar_Return = visitar_Return
    # Bloque 6: impresión
    visitar_Imprimir = visitar_Imprimir
    # Bloque 7: match
    visitar_Match = visitar_Match
    # Bloque 8: arreglos
    arreglo_literal = arreglo_literal
    visitar_AccederIndice = visitar_AccederIndice
    visitar_AsignarIndice = visitar_AsignarIndice
    visitar_Repetidor = visitar_Repetidor
    direccion_elemento = direccion_elemento
    guardar_en_direccion = guardar_en_direccion
    # Bloque 9: strings y embebidas
    visitar_DeclaracionString = visitar_DeclaracionString
    visitar_FuncionEmbebida = visitar_FuncionEmbebida

def generar_arm64(programa, tabla):
    """programa.s de un AST que el checker ya validó sin errores."""
    return GeneradorARM64(tabla).generar(programa)
