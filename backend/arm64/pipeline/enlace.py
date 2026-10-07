import re
from backend.arm64.pipeline.biblioteca import biblioteca
from backend.arm64.pipeline.carpetas import BINARIO, OBJETO
from backend.arm64.pipeline.herramientas import LD, correr

def enlazar(resultado):
    resultado.etapa = 'enlace'
    try:
        ruta_biblioteca = biblioteca()
    except RuntimeError as error:
        resultado.errores.append((0, 0, f'[Generacion] No se pudo construir liboxigen.a: {error}'))
        return False
    proceso = correr([LD, '-o', BINARIO, OBJETO, str(ruta_biblioteca)], resultado.carpeta)
    if proceso.returncode != 0:
        resultado.errores.append((0, 0, f'[Generacion] ld: {traducir_ld(proceso.stderr)}'))
        return False
    return True

def traducir_ld(stderr):
    # "/usr/bin/aarch64-linux-gnu-ld: programa.o: in function `main':" + "(.text+0x0): undefined ..."
    partes = [re.sub(r'^\S*ld: ', '', linea).strip() for linea in stderr.splitlines()]
    return ' '.join(parte for parte in partes if parte)
