import re
from backend.arm64.pipeline.carpetas import FUENTE, OBJETO
from backend.arm64.pipeline.herramientas import correr
from backend.arm64.runtime import AS, LIB

_ERROR_AS = re.compile(r'^programa\.s:(\d+): Error: (.*)$')
_ETIQUETA = re.compile(r'^([A-Za-z_.][\w.]*):')

def ensamblar(resultado):
    # cwd en la carpeta: as nombra el archivo como "programa.s" en sus mensajes
    proceso = correr([AS, '-I', str(LIB), '-o', OBJETO, FUENTE], resultado.carpeta)
    if proceso.returncode != 0:
        resultado.errores.extend(traducir_as(proceso.stderr, resultado.asm))
        return False
    return True

def traducir_as(stderr, asm):
    """Cada 'programa.s:N: Error: ...' con la etiqueta que contiene la línea y su instrucción."""
    lineas = asm.splitlines()
    errores = []
    for linea in stderr.splitlines():
        coincidencia = _ERROR_AS.match(linea)
        if not coincidencia:
            continue
        numero, mensaje = int(coincidencia.group(1)), coincidencia.group(2)
        texto = lineas[numero - 1].strip() if 0 < numero <= len(lineas) else ''
        errores.append((0, 0, f'[Generacion] as, programa.s línea {numero} '
                              f'(en {_etiqueta_contenedora(lineas, numero)}): {mensaje}. '
                              f'Instrucción: {texto}'))
    return errores or [(0, 0, f'[Generacion] as: {stderr.strip()}')]

def _etiqueta_contenedora(lineas, numero):
    for linea in reversed(lineas[:numero - 1]):
        coincidencia = _ETIQUETA.match(linea)
        if coincidencia:
            return coincidencia.group(1)
    return 'el inicio del archivo'
