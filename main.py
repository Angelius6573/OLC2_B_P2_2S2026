import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'backend'))

from backend.analizador_sintactico import parser
from backend.visitar_nodos import VisitarNodos

codigo = '''
struct StructWaos {
    x: i32,
    y: z,
}

fn main() {
    println!("Hello World", -x + 2, y);
}

fn foo(x: i32, y: f64) -> i32 { }
'''

result = parser.parse(codigo)
VisitarNodos().visitar(result)
#print(result)
