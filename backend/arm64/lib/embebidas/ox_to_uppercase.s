// ox_to_uppercase(x0 = puntero, x1 = longitud) -> x0 = bloque nuevo en mayúsculas, x1 = longitud
// Cambia a-z y el bloque Latin-1 de dos bytes U+00E0..U+00FE (C3 A0..C3 BE, menos C3 B7 '÷'),
// que en UTF-8 solo difiere en el segundo byte: á (C3 A1) -> Á (C3 81), ñ (C3 B1) -> Ñ (C3 91).
// La longitud en bytes no cambia.
.global ox_to_uppercase

.section .text
ox_to_uppercase:
  stp x29, x30, [sp, #-48]!
  mov x29, sp
  stp x0, x1, [x29, #16]
  mov x0, x1
  bl ox_reservar
  str x0, [x29, #32]

  ldp x9, x10, [x29, #16]         // x9 = origen, x10 = longitud
  mov x11, #0                     // x11 = posición
  mov w13, #0                     // w13 = byte anterior del origen

mayusculas_byte:
  cmp x11, x10
    b.hs mayusculas_fin
  ldrb w12, [x9, x11]
  mov w15, w12                    // w15 = byte original, será el anterior del siguiente
  sub w14, w12, #0x61             // 'a'
  cmp w14, #25
    b.hi mayusculas_latin
  sub w12, w12, #0x20
    b mayusculas_escribir

mayusculas_latin:
  cmp w13, #0xC3
    b.ne mayusculas_escribir
  sub w14, w12, #0xA0
  cmp w14, #0x1E
    b.hi mayusculas_escribir
  cmp w12, #0xB7
    b.eq mayusculas_escribir
  sub w12, w12, #0x20

mayusculas_escribir:
  strb w12, [x0, x11]
  mov w13, w15
  add x11, x11, #1
    b mayusculas_byte

mayusculas_fin:
  ldr x1, [x29, #24]
  ldp x29, x30, [sp], #48
  ret
