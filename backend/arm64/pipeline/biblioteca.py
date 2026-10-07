import threading
from backend.arm64.pipeline.carpetas import BUILD
from backend.arm64.runtime import LIB, NOMBRE_BIBLIOTECA, construir_biblioteca

_candado = threading.Lock()

def biblioteca():
    """liboxigen.a en build/arm64/, reconstruida si algún .s de lib/ es más reciente."""
    destino = BUILD / NOMBRE_BIBLIOTECA
    with _candado:
        ultima = max(fuente.stat().st_mtime for fuente in LIB.rglob('*.s'))
        if not destino.exists() or destino.stat().st_mtime < ultima:
            construir_biblioteca(BUILD)
    return destino
