use std::any::type_name_of_val;

use rand::Rng;

struct Persona {
    edad: i32,
    altura: f64,
}

fn main() {
    let saludo = String::from("Hola");
    let a: i32 = 10;
    let b: i32 = 15;
    let c: bool = true;
    let d: bool = false;
    let mut datos = vec![10, 20, 30];

    let name = String::from("ANGEL");

    let separador = String::from("Hola Mundo");
    let separado = separador.split(" ");

    datos.reverse();
    let waos = type_name_of_val(&name);

    let persona = Persona {
        edad: 18,
        altura: 164.8,
    };

    println!(
        "{} {} {} {} {} {} {:?} {} {} {} {} {} {} {:?} {} {}",
        saludo,
        a + b - a * b / a,
        a == b,
        c || d,
        sumar(a, b),
        saludo.replace("Hola", "OxigenScript"),
        datos,
        rand::thread_rng().gen_range(a..b),
        String::from("Waos"),
        datos[1],
        persona.edad,
        persona.altura,
        name.to_lowercase(),
        separado,
        name.contains("A"),
        waos
    );
}

fn sumar(x: i32, y: i32) -> i32 {
    x + y
}
