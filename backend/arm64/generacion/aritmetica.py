from backend.arm64.errores import ErrorGeneracion
from backend.arm64.generacion.tipos import es_par, posicion

ARITMETICOS = ('+', '-', '*', '/', '%')
RELACIONALES = ('==', '!=', '<', '<=', '>', '>=')

# cset tras cmp entre enteros (con signo) y tras fcmp entre flotantes
CONDICION_ENTERA = {'==': 'eq', '!=': 'ne', '<': 'lt', '<=': 'le', '>': 'gt', '>=': 'ge'}
CONDICION_FLOTANTE = {'==': 'eq', '!=': 'ne', '<': 'mi', '<=': 'ls', '>': 'gt', '>=': 'ge'}

INSTRUCCION_ENTERA = {'+': 'add', '-': 'sub', '*': 'mul'}
INSTRUCCION_FLOTANTE = {'+': 'fadd', '-': 'fsub', '*': 'fmul', '/': 'fdiv'}

def visitar_OperacionBinaria(self, nodo):
    if nodo.operador in ('&&', '||'):
        _logica(self, nodo)
        return
    tipo_izquierda = self.tipo(nodo.izquierda)
    tipo_derecha = self.tipo(nodo.derecha)
    self.visitar(nodo.izquierda)
    temporal = self.temporal()
    self.guardar_slot(temporal, es_par(tipo_izquierda), comentario='operando izquierdo')
    self.visitar(nodo.derecha)
    self.operar_binaria(nodo.operador, temporal, tipo_izquierda, tipo_derecha, nodo.tipo, nodo)

def operar_binaria(self, operador, temporal, tipo_izquierda, tipo_derecha, tipo_resultado, nodo):
    """Aplica el operador con el izquierdo en el temporal y el derecho en x0/x1.

    Izquierdo en x9/x10, derecho en x11/x12. El resultado queda en x0/x1.
    """
    e = self.e
    e.instr('mov', 'x11', 'x0')
    if es_par(tipo_derecha):
        e.instr('mov', 'x12', 'x1')
    self.cargar_slot(temporal, es_par(tipo_izquierda), 'x9', 'x10')

    if operador in RELACIONALES:
        if tipo_izquierda == 'String':
            _comparar_textos(self, operador)
        elif 'f64' in (tipo_izquierda, tipo_derecha):
            _a_flotantes(self, tipo_izquierda, tipo_derecha)
            e.instr('fcmp', 'd0', 'd1')
            e.instr('cset', 'x0', CONDICION_FLOTANTE[operador])
        else:
            # i32, char y bool se comparan como enteros
            e.instr('cmp', 'x9', 'x11')
            e.instr('cset', 'x0', CONDICION_ENTERA[operador])
        return
    if operador not in ARITMETICOS:
        raise ErrorGeneracion(f"Operador '{operador}' no soportado en ARM64", *posicion(nodo))

    if tipo_resultado == 'String':
        _aritmetica_textos(self, operador, tipo_izquierda, nodo)
    elif tipo_resultado == 'f64':
        _aritmetica_flotante(self, operador, tipo_izquierda, tipo_derecha, nodo)
    elif tipo_resultado == 'i32':
        _aritmetica_entera(self, operador, nodo)
    else:
        raise ErrorGeneracion(f"No se puede aplicar '{operador}' con resultado '{tipo_resultado}'",
                              *posicion(nodo))

def _aritmetica_entera(self, operador, nodo):
    e = self.e
    if operador in INSTRUCCION_ENTERA:
        e.instr(INSTRUCCION_ENTERA[operador], 'x0', 'x9', 'x11')
    else:
        _verificar_divisor_entero(self, operador, nodo)
        if operador == '/':
            e.instr('sdiv', 'w0', 'w9', 'w11', comentario='trunca hacia cero: solo la parte entera')
        else:
            # Módulo con piso: el resultado lleva el signo del divisor (-7 % 2 = 1, 7 % -2 = -1).
            # sdiv trunca, así que un resto distinto de cero con otro signo se corrige sumando el divisor
            e.instr('sdiv', 'w13', 'w9', 'w11')
            e.instr('msub', 'w0', 'w13', 'w11', 'w9', comentario='resto truncado')
            e.instr('eor', 'w14', 'w0', 'w11', comentario='bit 31: signos distintos')
            e.instr('cmp', 'w0', '#0')
            e.instr('ccmp', 'w14', '#0', '#0', 'ne', comentario='resto 0: no se corrige')
            e.instr('csel', 'w14', 'w11', 'wzr', 'lt')
            e.instr('add', 'w0', 'w0', 'w14', comentario='módulo con el signo del divisor')
    # Un i32 vive extendido en signo: el resultado envuelve en 32 bits
    e.instr('sxtw', 'x0', 'w0')

def _verificar_divisor_entero(self, operador, nodo):
    valido = f'divisor_valido_{self.nuevo_numero()}'
    self.e.instr('cbnz', 'w11', valido)
    self.error_runtime('ERR_DIVISION_CERO' if operador == '/' else 'ERR_MODULO_CERO', nodo)
    self.e.etiqueta(valido)

def _a_flotantes(self, tipo_izquierda, tipo_derecha):
    # Promoción de tipos: un i32 mezclado con un f64 se convierte
    e = self.e
    if tipo_izquierda == 'i32':
        e.instr('scvtf', 'd0', 'x9')
    else:
        e.instr('fmov', 'd0', 'x9')
    if tipo_derecha == 'i32':
        e.instr('scvtf', 'd1', 'x11')
    else:
        e.instr('fmov', 'd1', 'x11')

def _aritmetica_flotante(self, operador, tipo_izquierda, tipo_derecha, nodo):
    e = self.e
    _a_flotantes(self, tipo_izquierda, tipo_derecha)
    if operador in ('/', '%'):
        # Igual que el intérprete: dividir un f64 entre cero es error, no infinito
        valido = f'divisor_valido_{self.nuevo_numero()}'
        e.instr('fcmp', 'd1', '#0.0')
        e.instr('b.ne', valido)
        self.error_runtime('ERR_DIVISION_CERO' if operador == '/' else 'ERR_MODULO_CERO', nodo)
        e.etiqueta(valido)
    if operador == '%':
        # Módulo con piso: a - floor(a / b) * b, con el signo del divisor, igual que en i32
        e.instr('fdiv', 'd2', 'd0', 'd1')
        e.instr('frintm', 'd2', 'd2', comentario='piso del cociente')
        e.instr('fmsub', 'd0', 'd2', 'd1', 'd0')
    else:
        e.instr(INSTRUCCION_FLOTANTE[operador], 'd0', 'd0', 'd1')
    e.instr('fmov', 'x0', 'd0')

def _comparar_textos(self, operador):
    e = self.e
    e.instr('mov', 'x0', 'x9')
    e.instr('mov', 'x1', 'x10')
    e.instr('mov', 'x2', 'x11')
    e.instr('mov', 'x3', 'x12')
    e.instr('bl', 'ox_comparar_texto')
    e.instr('cmp', 'x0', '#0')
    e.instr('cset', 'x0', CONDICION_ENTERA[operador])

def _aritmetica_textos(self, operador, tipo_izquierda, nodo):
    e = self.e
    if operador == '+':
        e.instr('mov', 'x0', 'x9')
        e.instr('mov', 'x1', 'x10')
        e.instr('mov', 'x2', 'x11')
        e.instr('mov', 'x3', 'x12')
        e.instr('bl', 'ox_concatenar')
    elif operador == '*':
        # String * i32 o i32 * String: el texto repetido n veces
        if tipo_izquierda == 'String':
            e.instr('mov', 'x0', 'x9')
            e.instr('mov', 'x1', 'x10')
            e.instr('mov', 'x2', 'x11')
        else:
            e.instr('mov', 'x0', 'x11')
            e.instr('mov', 'x1', 'x12')
            e.instr('mov', 'x2', 'x9')
        e.instr('bl', 'ox_repetir')
    else:
        raise ErrorGeneracion(f"No se puede aplicar '{operador}' a String", *posicion(nodo))

def _logica(self, nodo):
    # Corto circuito obligatorio: el derecho no se evalúa si el izquierdo decide
    fin = f'fin_logico_{self.nuevo_numero()}'
    self.visitar(nodo.izquierda)
    self.e.instr('cbz' if nodo.operador == '&&' else 'cbnz', 'x0', fin)
    self.visitar(nodo.derecha)
    self.e.etiqueta(fin)

def visitar_OperacionUnaria(self, nodo):
    self.visitar(nodo.derecha)
    if nodo.operador == '!':
        self.e.instr('eor', 'x0', 'x0', '#1')
    elif nodo.tipo == 'f64':
        self.e.instr('fmov', 'd0', 'x0')
        self.e.instr('fneg', 'd0', 'd0')
        self.e.instr('fmov', 'x0', 'd0')
    else:
        self.e.instr('neg', 'x0', 'x0')
        self.e.instr('sxtw', 'x0', 'w0')
