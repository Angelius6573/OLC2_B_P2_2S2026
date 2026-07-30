import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'backend'))

from backend.analizador_sintactico import parser

codigo = '''
fn main(waos, c) {
    println!("Hello World!");
}
'''

result = parser.parse(codigo)
print("Resultados:\n")
print(result)
