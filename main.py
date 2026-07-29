import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'backend'))

from backend.analizador_sintactico import parser
from backend.analizador_lexico import lexer

codigo = 'println!("x = {}", c + 1)'

result = parser.parse(codigo)
print("Resultados:\n")
print(result)
