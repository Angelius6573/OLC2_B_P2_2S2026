import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class ResultadoARM64:
    """Lo que devuelve el pipeline. Los errores son tuplas (linea, columna, '[Categoría] mensaje'),
    el mismo formato de backend/errores.py:
    - [Generacion]: el generador no soporta el programa, o as / ld rechazan programa.s.
    - [Ejecucion]: lo que ox_error escribe en stderr, una señal o el tiempo límite.
    """
    etapa: str = 'generacion'       # generacion, ensamblado, enlace o ejecucion: la última alcanzada
    exito: bool = False             # se ejecutó y terminó con código 0
    asm: str = ''
    salida: str = ''
    salida_errores: str = ''        # stderr tal cual
    codigo_salida: int | None = None
    errores: list = field(default_factory=list)
    tiempos: dict = field(default_factory=dict)     # milisegundos por etapa
    carpeta: Path | None = None

@contextmanager
def cronometro(resultado, etapa):
    inicio = time.perf_counter()
    try:
        yield
    finally:
        resultado.tiempos[etapa] = round((time.perf_counter() - inicio) * 1000, 1)
