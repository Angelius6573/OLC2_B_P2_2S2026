fn factorial(n: i32) -> i32 {
    if n <= 1 {
        return 1;
    }
    return n * factorial(n - 1);
}

fn main() {
    let nombre = String::from("OxigenNative");
    let numeros: [i32; 5] = [3, 1, 4, 1, 5];
    let mut suma = 0;
    for n in numeros {
        suma += n;
    }
    let promedio: f64 = 2.8;
    println!("Hola desde {}", nombre);
    println!("Suma: {}, promedio: {}", suma, promedio);
    println!("factorial(5) = {}", factorial(5));
    println!("{:?}", numeros);
}
