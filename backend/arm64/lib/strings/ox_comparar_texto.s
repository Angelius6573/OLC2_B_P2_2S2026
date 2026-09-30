// ox_comparar_texto(x0 = puntero 1, x1 = longitud 1, x2 = puntero 2, x3 = longitud 2)
//   -> x0 = -1 si texto 1 < texto 2, 0 si son iguales, 1 si texto 1 > texto 2
// Orden lexicográfico por bytes; a igual prefijo, el más corto va primero.
.global ox_comparar_texto

.section .text
ox_comparar_texto:
  mov x9, #0                      // x9 = posición
  cmp x1, x3
  csel x10, x1, x3, lo            // x10 = longitud más corta

comparar_byte:
  cmp x9, x10
    b.hs comparar_longitudes
  ldrb w11, [x0, x9]
  ldrb w12, [x2, x9]
  cmp w11, w12
    b.lo comparar_menor
    b.hi comparar_mayor
  add x9, x9, #1
    b comparar_byte

comparar_longitudes:
  cmp x1, x3
    b.lo comparar_menor
    b.hi comparar_mayor
  mov x0, #0
  ret

comparar_menor:
  mov x0, #-1
  ret

comparar_mayor:
  mov x0, #1
  ret
