import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.analizador_sintactico import parser
from backend.errores import errores, limpiar
from backend.analizador_semantico import AnalizadorSemantico
from backend.visitor.grafo import VisitarGrafo
from backend.reportes.errores import filas_errores
from backend.reportes.simbolos import filas_simbolos
from backend.reportes.simbolos_html import escribir_reporte
from api.estado import estado_ejecucion, estado_sin_ejecutar
from api.modo_arm64 import ejecutar_arm64, ejecutar_con_errores_semanticos
from api.modo_interprete import ejecutar_interprete

def compilar_codigo(codigo: str, modo: str = 'arm64') -> dict:
    """Análisis, reportes y ejecución en el modo pedido.

    En modo intérprete el flujo es el de la Fase 1: se ejecuta aunque haya errores semánticos.
    En modo ARM64 solo se genera código para un programa sin errores. Con errores semánticos, pero
    sin léxicos ni sintácticos, se ejecuta con el intérprete; con estos últimos no se ejecuta.
    """
    limpiar()
    programa = parser.parse(codigo)
    errores_lex_sin = list(errores)
    respuesta = {'mode': modo, 'output': '', 'errors': [], 'symbols': [], 'symbols_report': None,
                 'ast_image': None, 'arm64': None, 'status': estado_sin_ejecutar(bool(errores_lex_sin))}
    if programa is None:
        respuesta['errors'] = filas_errores(errores_lex_sin, codigo)
        return respuesta

    analizador = AnalizadorSemantico()
    analizador.analizar(programa)
    errores_semanticos = list(analizador.errores)

    grafo = VisitarGrafo()
    grafo.visitar(programa)
    respuesta['ast_image'] = grafo.renderizar()

    celdas = {}
    errores_ejecucion = []
    ejecucion = None
    if modo == 'interprete':
        salida, errores_ejecucion, celdas, tiempo = ejecutar_interprete(programa, analizador.tabla)
        respuesta['output'] = salida
        ejecucion = ('interprete', None, tiempo)
    elif not errores_lex_sin:
        ejecutar = ejecutar_con_errores_semanticos if errores_semanticos else ejecutar_arm64
        salida, errores_ejecucion, celdas, arm64, modo_real = ejecutar(programa, analizador.tabla)
        tiempo = arm64['times'].get('ejecucion', arm64['times'].get('interprete'))
        respuesta.update(output=salida, arm64=arm64)
        ejecucion = (modo_real, arm64, tiempo)

    filas = filas_errores(errores_lex_sin + errores_semanticos + errores_ejecucion, codigo)
    respuesta['errors'] = filas
    if ejecucion is not None:
        respuesta['status'] = estado_ejecucion(modo, *ejecucion, filas)
    else:
        respuesta['status'] = estado_sin_ejecutar(True)

    simbolos = filas_simbolos(analizador.tabla, celdas)
    respuesta['symbols'] = simbolos
    respuesta['symbols_report'] = escribir_reporte(simbolos)
    return respuesta
