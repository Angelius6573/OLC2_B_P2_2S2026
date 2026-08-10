fn main() {
    let num: i32 = 5;
    let mut texto = String::from("Hola Mundo");
    texto.push_str(" Waos");
    let text = texto.replace("Mundo", "Rust");
    let c: usize = texto.len();
    let prueba = num;

    println!("{} <-> {}, {} ?? {}", texto, text, c, prueba);
}
