import re
import resource
import signal
import subprocess
from backend.arm64.pipeline.carpetas import BINARIO
from backend.arm64.pipeline.herramientas import QEMU

TIEMPO_LIMITE = 10              # segundos de qemu antes de detener el programa
_ERROR_RUNTIME = re.compile(r'^\[Ejecucion\] Línea (\d+), Columna (\d+): (.*)$')

def ejecutar(resultado, tiempo_limite):
    resultado.etapa = 'ejecucion'
    try:
        proceso = subprocess.run([QEMU, f'./{BINARIO}'], cwd=resultado.carpeta, capture_output=True, timeout=tiempo_limite, 
                                 preexec_fn=_sin_core)
    except subprocess.TimeoutExpired as expirado:
        resultado.salida = _decodificar(expirado.stdout)
        resultado.salida_errores = _decodificar(expirado.stderr)
        resultado.errores.extend(errores_runtime(resultado.salida_errores))
        resultado.errores.append((0, 0, f'[Ejecucion] El programa no terminó en {tiempo_limite} s y se detuvo'))
        return
    resultado.salida = _decodificar(proceso.stdout)
    resultado.salida_errores = _decodificar(proceso.stderr)
    resultado.codigo_salida = proceso.returncode
    resultado.errores.extend(errores_runtime(resultado.salida_errores))
    if proceso.returncode < 0:
        nombre = signal.Signals(-proceso.returncode).name
        resultado.errores.append((0, 0, f'[Ejecucion] El programa terminó por la señal {nombre}'))
    elif proceso.returncode > 0 and not resultado.errores:
        resultado.errores.append((0, 0, f'[Ejecucion] El programa terminó con código ' f'{proceso.returncode}'))
    resultado.exito = proceso.returncode == 0

def errores_runtime(stderr):
    """Las líneas de ox_error con la posición del .ox; los avisos propios de qemu se omiten."""
    errores = []
    for linea in stderr.splitlines():
        coincidencia = _ERROR_RUNTIME.match(linea)
        if coincidencia:
            errores.append((int(coincidencia.group(1)), int(coincidencia.group(2)), f'[Ejecucion] {coincidencia.group(3)}'))
        elif linea.strip() and not linea.startswith('qemu:'):
            errores.append((0, 0, f'[Ejecucion] {linea}'))
    return errores

def _sin_core():
    # qemu escribe un core dump en la carpeta si el programa recibe SIGSEGV
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))

def _decodificar(datos):
    if datos is None:
        return ''
    return datos.decode('utf-8', errors='replace') if isinstance(datos, bytes) else datos
