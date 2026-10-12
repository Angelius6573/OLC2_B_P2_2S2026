import contextlib
import io
import re
import time

from backend.errores import errores
from backend.reportes.interprete_valores import InterpreteConValores, LimitePasos

_POSICION = re.compile(r'^\[Ejecucion\] (\d+):(\d+) (.*)$', re.DOTALL)

def ejecutar_interprete(programa, tabla, limite_pasos=None):
    """Ejecuta con el intérprete. Devuelve salida, errores de ejecución, celdas por sym_id y ms."""
    interprete = InterpreteConValores(tabla, limite_pasos)
    inicio_errores = len(errores)
    salida = io.StringIO()
    propios = []
    inicio = time.perf_counter()
    try:
        # El stderr del intérprete repite lo que ya reportó en backend.errores
        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(io.StringIO()):
            interprete.ejecutar(programa)
    except SystemExit:
        pass
    except LimitePasos:
        propios.append((0, 0, f'[Ejecucion] El intérprete se detuvo tras {limite_pasos} pasos'))
    except Exception as e:
        propios.append((0, 0, f'[Ejecucion] {e}'))
    tiempo = round((time.perf_counter() - inicio) * 1000, 1)
    # Interprete.ejecutar reporta sus RuntimeError en backend.errores antes de salir
    de_ejecucion = [_con_posicion(e) for e in errores[inicio_errores:] if e[2].startswith('[Ejecucion]')]
    return salida.getvalue(), de_ejecucion + propios, interprete.celdas, tiempo

def _con_posicion(error):
    """El intérprete reporta en (0, 0) y escribe la posición al inicio del texto: '3:10 División por cero'."""
    linea, columna, mensaje = error
    coincidencia = _POSICION.match(mensaje)
    if linea or not coincidencia:
        return error
    texto = coincidencia.group(3)
    return int(coincidencia.group(1)), int(coincidencia.group(2)), f'[Ejecucion] {texto.rstrip(".")}.'
