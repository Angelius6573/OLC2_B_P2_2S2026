import struct

from backend.arm64.errores import ErrorGeneracion
from backend.arm64.generacion.tipos import posicion

def bits_f64(valor):
    return struct.unpack('<Q', struct.pack('<d', valor))[0]

def visitar_NumeroEntero(self, nodo):
    self.e.cargar_inmediato('x0', nodo.valor)

def visitar_NumeroFloat(self, nodo):
    # Un f64 viaja como sus bits IEEE-754 en x0 (desviación 2 de AAPCS64)
    bits = bits_f64(nodo.valor)
    if bits == 0:
        self.e.instr('mov', 'x0', '#0', comentario='0.0')
    else:
        self.e.instr('ldr', 'x0', f'={bits:#018x}', comentario=repr(nodo.valor))

def visitar_Booleano(self, nodo):
    self.e.instr('mov', 'x0', '#1' if nodo.valor else '#0', comentario='true' if nodo.valor else 'false')

def visitar_Caracter(self, nodo):
    if not isinstance(nodo.valor, str) or len(nodo.valor) != 1:
        raise ErrorGeneracion(f'Literal de carácter inválido: {nodo.valor!r}', *posicion(nodo))
    # Un char es su punto de código Unicode; ox_print_char lo codifica en UTF-8
    self.e.cargar_inmediato('x0', ord(nodo.valor), comentario=repr(nodo.valor))

def visitar_Cadena(self, nodo):
    # Un literal apunta a .rodata: {puntero, longitud} en x0 y x1
    self.cargar_texto(nodo.string)
