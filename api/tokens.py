import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.analizador_lexico import lexer, lexema_tipo, contar_columna


def obtener_tokens(codigo: str) -> list[dict]:
    lexer.input(codigo)
    tokens = []
    while (tok := lexer.token()) is not None:
        tokens.append({
            "type": tok.type,
            "lexema": lexema_tipo(tok.type),
            "value": str(tok.value),
            "line": tok.lineno,
            "col": contar_columna(codigo, tok),
        })
    return tokens
