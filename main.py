import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'backend'))

from backend.analizador_sintactico import parser
from backend.visitor.grafo import VisitarGrafo

codigo = '''
struct Persona {
    nombre: String,
    edad: i32,
    activo: bool,
}

struct Coordenada {
    x: i32,
    y: i32,
}

fn operar(a: i32, b: i32) -> i32 {
    let parcial = a + b;
    parcial;
}

fn main() {
    // Literales y declaraciones tipadas/sin tipo
    let mut contador: i32 = 0;
    let flotante: f64 = 3.14;
    let caracter: char = 'A';
    let activo: bool = true;
    let numero = 42;
    let cadena_corta = "hola";
    let cadena_cruda = r#"texto crudo"#;
    let vacia = String::new();

    // Strings: creacion, modificacion y funciones embebidas
    let saludo = String::from("Hola");
    saludo.push_str(", mundo!");
    let texto = saludo.to_uppercase();
    let minus = saludo.to_lowercase();
    let inverso = saludo.reverse();
    let con_a = saludo.contains("a");
    let reemplazado = saludo.replace("a", "o");
    let partes = saludo.split(" ");
    let longitud = saludo.len();

    // Aritmetica, relacionales y logicas
    let aritmetica = (contador + 5) * 2 - 1 / 2 % 3;
    let negativo = -aritmetica + 2;
    let relacional = contador >= 1 && contador != 5 || !activo;
    let comparacion = contador == 0;

    // Funciones embebidas de alcance global
    let tipo = typeof(contador);
    let azar = random(1, 100);

    // Arreglos: declaracion, inicializacion e indices
    let numeros: [i32; 4] = [1, 2, 3, 4];
    let matriz = [[1, 2], [3, 4]];
    let primero = numeros[0];
    let cruzado = matriz[1][0];

    // Structs: instanciacion y acceso a campos
    let persona = Persona { nombre: "Ana", edad: 25, activo: true, };
    let punto = Coordenada { x: 3, y: 4, };
    let nombre = persona.nombre;
    let anidado = persona.edad;

    // Llamadas a funcion y asignaciones
    operar(contador, 5);
    contador = contador + 1;
    contador + 1;

    // Impresion
    println!("Hello World");
    println!("Hola {}, tienes {} anios", persona.nombre, persona.edad);
    println!("{}", aritmetica, negativo, relacional, comparacion);
    println!("{}", azar, tipo, primero, cruzado, nombre, anidado, longitud);
    println!("{}", texto, minus, inverso, con_a, reemplazado, partes, cadena_cruda);
}
'''

codigo_test_sencillo = '''

'''

result = parser.parse(codigo_test_sencillo)
visitar_nodos_graph = VisitarGrafo()
visitar_nodos_graph.visitar(result)
visitar_nodos_graph.renderizar()
#VisitarGrafo().visitar(result)
#print(result)
