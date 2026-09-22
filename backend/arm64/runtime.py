import subprocess
from pathlib import Path

LIB = Path(__file__).parent / 'lib'
NOMBRE_BIBLIOTECA = 'liboxigen.a'

AS = 'aarch64-linux-gnu-as'
AR = 'aarch64-linux-gnu-ar'

def fuentes_runtime():
    # Una rutina por archivo: lib/<tema>/ox_<rutina>.s. var_globs.s se incluye, no se ensambla
    return sorted(LIB.rglob('ox_*.s'))

def construir_biblioteca(destino):
    """Ensambla cada rutina y las empaqueta en liboxigen.a dentro de `destino`.

    ld solo extrae de una biblioteca estática los objetos que el programa usa, así que el
    binario lleva únicamente las rutinas ox_* que se llaman, directa o indirectamente.
    """
    destino = Path(destino)
    objetos = destino / 'runtime'
    objetos.mkdir(parents=True, exist_ok=True)
    rutas_objeto = []
    for fuente in fuentes_runtime():
        objeto = objetos / f'{fuente.stem}.o'
        _ejecutar([AS, '-I', str(LIB), '-o', str(objeto), str(fuente)])
        rutas_objeto.append(str(objeto))
    biblioteca = destino / NOMBRE_BIBLIOTECA
    biblioteca.unlink(missing_ok=True)
    _ejecutar([AR, 'rcs', str(biblioteca), *rutas_objeto])
    return biblioteca

def _ejecutar(comando):
    resultado = subprocess.run(comando, capture_output=True, text=True)
    if resultado.returncode != 0:
        raise RuntimeError(f'Falló {Path(comando[0]).name}:\n{resultado.stderr}')
