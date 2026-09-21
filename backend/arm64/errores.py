import re
from pathlib import Path

RUTA_VAR_GLOBS = Path(__file__).parent / 'lib' / 'var_globs.s'

_EQU = re.compile(r'^\s*\.equ\s+(\w+)\s*,\s*(\S+)')

class ErrorGeneracion(Exception):
    # El programa no se puede compilar a ARM64. Nunca se emite código a medias
    def __init__(self, mensaje, linea=0, columna=0):
        super().__init__(mensaje)
        self.linea = linea
        self.columna = columna

def leer_constantes(ruta=RUTA_VAR_GLOBS):
    constantes = {}
    for linea in Path(ruta).read_text(encoding='utf-8').splitlines():
        coincidencia = _EQU.match(linea)
        if coincidencia:
            constantes[coincidencia.group(1)] = int(coincidencia.group(2), 0)
    return constantes

# Los códigos se leen de var_globs.s para que Python y el runtime no se desincronicen
CODIGOS_ERROR = {nombre: valor for nombre, valor in leer_constantes().items()
                 if nombre.startswith('ERR_') and nombre != 'ERR_ULTIMO'}

def emitir_error_runtime(emisor, codigo, linea, columna):
    """mov x6, código + bl ox_error. El llamador emite después el salto a la siguiente sentencia."""
    if codigo not in CODIGOS_ERROR:
        raise ErrorGeneracion(f'Código de error de runtime desconocido: {codigo}')
    emisor.instr('mov', 'x6', codigo)
    emisor.cargar_inmediato('x0', linea, comentario='línea')
    emisor.cargar_inmediato('x1', columna, comentario='columna')
    emisor.instr('bl', 'ox_error')
