import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'backend'))

from backend.analizador_sintactico import parser
from backend.errores import errores, limpiar
from backend.analizador_semantico import AnalizadorSemantico
from backend.interpreter.interprete import Interprete
from backend.visitor.grafo import VisitarGrafo

codigo_sencillo = '''
fn main(){
ç
len
    let texto = String::from(r#"Él dijo: "Hola Rust""#);
    println!("{}", texto);
}
'''

def compilar(codigo_sencillo):
    limpiar()
    result = parser.parse(codigo_sencillo)
    if result is None:
        for linea, columna, mensaje in errores:
            print(f"{linea}:{columna} {mensaje}")
        sys.exit(1)

    analizador = AnalizadorSemantico()
    analizador.analizar(result)

    errores_lex_syn = list(errores)
    errores_sem = list(analizador.errores)
    for linea, col, msg in errores_lex_syn + errores_sem:
        print(f"{linea}:{col} {msg}")

    print("Compilación exitosa")
    visitar_nodos_graph = VisitarGrafo()
    visitar_nodos_graph.visitar(result)
    ast_file = visitar_nodos_graph.renderizar()

    Interprete().ejecutar(result)

compilar(codigo_sencillo)
