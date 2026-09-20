import sys
import io
import contextlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.analizador_sintactico import parser
from backend.errores import errores, limpiar
from backend.analizador_semantico import AnalizadorSemantico
from backend.interpreter.interprete import Interprete
from backend.visitor.grafo import VisitarGrafo


def compilar_codigo(codigo: str) -> dict:
    limpiar()

    result = parser.parse(codigo)

    errores_lex_sin = list(errores)

    if result is None:
        return {
            "output": "",
            "errors": [{"line": l, "col": c, "message": m} for l, c, m in errores_lex_sin],
            "symbols": [],
            "ast_image": None,
        }

    analizador = AnalizadorSemantico()
    analizador.analizar(result)

    errores_sem = list(analizador.errores)
    todos_errores = [{"line": l, "col": c, "message": m} for l, c, m in errores_lex_sin + errores_sem]

    grafo = VisitarGrafo()
    grafo.visitar(result)
    ast_file = grafo.renderizar()

    stdout_capture = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout_capture):
            Interprete().ejecutar(result)
    except SystemExit:
        pass
    except Exception as e:
        todos_errores.append({"line": 0, "col": 0, "message": f"[Ejecucion] {str(e)}"})

    return {
        "output": stdout_capture.getvalue(),
        "errors": todos_errores,
        "symbols": [],
        "ast_image": ast_file,
    }
