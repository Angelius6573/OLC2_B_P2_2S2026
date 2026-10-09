import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.analizador_sintactico import parser
from backend.errores import errores, limpiar
from backend.analizador_semantico import AnalizadorSemantico
from backend.visitor.grafo import VisitarGrafo
from backend.reportes.simbolos import filas_simbolos
from backend.reportes.simbolos_html import escribir_reporte
from api.estado import estado_ejecucion, estado_sin_ejecutar
from api.modo_arm64 import ejecutar_arm64
from api.modo_interprete import ejecutar_interprete

def compilar_codigo(codigo: str, modo: str = 'arm64') -> dict:
    """Análisis, reportes y ejecución en el modo pedido.

    En modo intérprete el flujo es el de la Fase 1: se ejecuta aunque haya errores semánticos.
    En modo ARM64 solo se genera código para un programa sin errores.
    """
    limpiar()
    programa = parser.parse(codigo)
    errores_lex_sin = list(errores)
    respuesta = {'mode': modo, 'output': '', 'errors': [], 'symbols': [], 'symbols_report': None,
                 'ast_image': None, 'arm64': None, 'status': estado_sin_ejecutar(bool(errores_lex_sin))}
    if programa is None:
        respuesta['errors'] = _json(errores_lex_sin)
        return respuesta

    analizador = AnalizadorSemantico()
    analizador.analizar(programa)
    errores_previos = errores_lex_sin + list(analizador.errores)

    grafo = VisitarGrafo()
    grafo.visitar(programa)
    respuesta['ast_image'] = grafo.renderizar()

    celdas = {}
    errores_ejecucion = []
    if modo == 'interprete':
        salida, errores_ejecucion, celdas, tiempo = ejecutar_interprete(programa, analizador.tabla)
        respuesta['output'] = salida
        respuesta['status'] = estado_ejecucion(modo, 'interprete', None, errores_ejecucion, tiempo)
    elif not errores_previos:
        salida, errores_ejecucion, celdas, arm64, modo_real = ejecutar_arm64(programa, analizador.tabla)
        tiempo = arm64['times'].get('ejecucion', arm64['times'].get('interprete'))
        respuesta.update(output=salida, arm64=arm64)
        respuesta['status'] = estado_ejecucion(modo, modo_real, arm64, errores_ejecucion, tiempo)
    else:
        respuesta['status'] = estado_sin_ejecutar(True)

    simbolos = filas_simbolos(analizador.tabla, celdas)
    respuesta['symbols'] = simbolos
    respuesta['symbols_report'] = escribir_reporte(simbolos)
    respuesta['errors'] = _json(errores_previos + errores_ejecucion)
    return respuesta


def _json(errores_tuplas):
    return [{'line': l, 'col': c, 'message': m} for l, c, m in errores_tuplas]
