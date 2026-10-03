// ox_reverse(x0 = puntero, x1 = longitud) -> x0 = bloque nuevo con el texto invertido, x1 = longitud
// Invierte por caracteres, no por bytes: cada carácter UTF-8 se copia entero desde el final del
// bloque hacia el inicio, así que "año" da "oña" y no bytes sueltos.
.global ox_reverse

.section .text
ox_reverse:
  stp x29, x30, [sp, #-48]!
  mov x29, sp
  stp x0, x1, [x29, #16]
  mov x0, x1
  bl ox_reservar
  str x0, [x29, #32]

  ldp x9, x10, [x29, #16]         // x9 = origen, x10 = longitud
  mov x11, #0                     // x11 = posición en el origen
  mov x12, x10                    // x12 = fin libre en el destino

invertir_caracter:
  cmp x11, x10
    b.hs invertir_fin
  // Longitud del carácter según su primer byte
  ldrb w13, [x9, x11]
  mov x14, #1
  cmp w13, #0xC0
    b.lo invertir_longitud
  mov x14, #2
  cmp w13, #0xE0
    b.lo invertir_longitud
  mov x14, #3
  cmp w13, #0xF0
    b.lo invertir_longitud
  mov x14, #4

invertir_longitud:
  // Un carácter cortado al final del texto se copia solo hasta donde llega
  add x15, x11, x14
  cmp x15, x10
    b.ls invertir_copiar
  sub x14, x10, x11

invertir_copiar:
  sub x12, x12, x14
  mov x15, #0

invertir_byte:
  add x5, x11, x15
  ldrb w13, [x9, x5]
  add x5, x12, x15
  strb w13, [x0, x5]
  add x15, x15, #1
  cmp x15, x14
    b.lo invertir_byte
  add x11, x11, x14
    b invertir_caracter

invertir_fin:
  ldr x1, [x29, #24]
  ldp x29, x30, [sp], #48
  ret
