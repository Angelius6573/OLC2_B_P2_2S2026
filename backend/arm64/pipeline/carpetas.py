import re
import shutil
import uuid
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
BUILD = RAIZ / 'build' / 'arm64'
FUENTE = 'programa.s'
OBJETO = 'programa.o'
BINARIO = 'programa'
CONSERVAR_EJECUCIONES = 20      # carpetas <uuid> que quedan en build/arm64/
_CARPETA_EJECUCION = re.compile(r'^[0-9a-f]{32}$')

def nueva_carpeta():
    """build/arm64/<uuid>/ para una ejecución. Borra las más viejas; f0/ y f2/ no se tocan."""
    BUILD.mkdir(parents=True, exist_ok=True)
    anteriores = sorted((c for c in BUILD.iterdir() if c.is_dir() and _CARPETA_EJECUCION.match(c.name)),
                        key=lambda c: c.stat().st_mtime)
    for vieja in anteriores[:max(0, len(anteriores) - CONSERVAR_EJECUCIONES + 1)]:
        shutil.rmtree(vieja, ignore_errors=True)
    return BUILD / uuid.uuid4().hex
