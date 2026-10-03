// ox_len(x0 = puntero, x1 = longitud en bytes) -> x0 = cantidad de caracteres
// Cuenta puntos de código UTF-8, como el intérprete: un byte de continuación (10xxxxxx) no
// empieza carácter. "año" tiene 4 bytes y 3 caracteres.
.global ox_len

.section .text
ox_len:
  mov x9, #0                      // x9 = posición
  mov x10, #0                     // x10 = caracteres

len_byte:
  cmp x9, x1
    b.hs len_fin
  ldrb w11, [x0, x9]
  and w11, w11, #0xC0
  cmp w11, #0x80
  cinc x10, x10, ne
  add x9, x9, #1
    b len_byte

len_fin:
  mov x0, x10
  ret
