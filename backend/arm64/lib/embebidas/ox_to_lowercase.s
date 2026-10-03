// ox_to_lowercase(x0 = puntero, x1 = longitud) -> x0 = bloque nuevo en minúsculas, x1 = longitud
// Cambia A-Z y el bloque Latin-1 de dos bytes U+00C0..U+00DE (C3 80..C3 9E, menos C3 97 '×'),
// que en UTF-8 solo difiere en el segundo byte: Á (C3 81) -> á (C3 A1), Ñ (C3 91) -> ñ (C3 B1).
// La longitud en bytes no cambia.
.global ox_to_lowercase

.section .text
ox_to_lowercase:
  stp x29, x30, [sp, #-48]!
  mov x29, sp
  stp x0, x1, [x29, #16]
  mov x0, x1
  bl ox_reservar
  str x0, [x29, #32]

  ldp x9, x10, [x29, #16]         // x9 = origen, x10 = longitud
  mov x11, #0                     // x11 = posición
  mov w13, #0                     // w13 = byte anterior del origen

minusculas_byte:
  cmp x11, x10
    b.hs minusculas_fin
  ldrb w12, [x9, x11]
  mov w15, w12                    // w15 = byte original, será el anterior del siguiente
  sub w14, w12, #0x41             // 'A'
  cmp w14, #25
    b.hi minusculas_latin
  add w12, w12, #0x20
    b minusculas_escribir

minusculas_latin:
  cmp w13, #0xC3
    b.ne minusculas_escribir
  sub w14, w12, #0x80
  cmp w14, #0x1E
    b.hi minusculas_escribir
  cmp w12, #0x97
    b.eq minusculas_escribir
  add w12, w12, #0x20

minusculas_escribir:
  strb w12, [x0, x11]
  mov w13, w15
  add x11, x11, #1
    b minusculas_byte

minusculas_fin:
  ldr x1, [x29, #24]
  ldp x29, x30, [sp], #48
  ret
