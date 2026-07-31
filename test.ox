fn main() {
    println!("Hello World!");

    let mut a: i32 = 10;
    let b: i32 = 20;
    let mut resultado: i32 = a + b * 3;
    println!("Resultado: {}", resultado);

    if a > b {
        println!("a es mayor que b");
    } else {
        println!("a no es mayor que b");
    }

    while a > 0 {
        println!("a = {}", a);
        a = a - 1;
    }

    for i in 0..5 {
        println!("i = {}", i);
    }

    let mut contador: i32 = 0;
    loop {
        println!("contador = {}", contador);
        contador = contador + 1;
        if contador >= 3 {
            break;
        }
    }

    let texto: String = "Rust";
    let longitud: i32 = len(texto);
    println!("Longitud: {}", longitud);

    let mayus: String = to_uppercase(texto);
    println!("Mayúsculas: {}", mayus);
}
