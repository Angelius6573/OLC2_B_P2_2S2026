// ox_split(x0 = texto, x1 = longitud, x2 = separador, x3 = longitud separador)
//   -> x0 = arreglo de celdas String, x1 = cantidad
// "a,,b".split(",") da ["a", "", "b"], como el intérprete. Cada celda apunta dentro del texto
// original, que nunca se modifica. Con el separador vacío devuelve [texto].
.global ox_split
.include "var_globs.s"

// Marco: texto 16, longitud 24, separador 32, longitud separador 40, posición 48,
// cantidad 56, arreglo 64, celda actual 72
.section .text
ox_split:
  stp x29, x30, [sp, #-80]!
  mov x29, sp
  stp x0, x1, [x29, #16]
  stp x2, x3, [x29, #32]
  str xzr, [x29, #48]
  mov x9, #1
  str x9, [x29, #56]
  cbz x3, split_reservar

split_contar:
  ldp x0, x1, [x29, #16]
  ldp x2, x3, [x29, #32]
  ldr x4, [x29, #48]
  bl ox_buscar_texto
  tbnz x0, #63, split_reservar
  ldr x9, [x29, #56]
  add x9, x9, #1
  str x9, [x29, #56]
  ldr x10, [x29, #40]
  add x0, x0, x10
  str x0, [x29, #48]
    b split_contar

split_reservar:
  ldr x0, [x29, #56]
  lsl x0, x0, #4                  // cantidad * TAMANIO_CELDA
  bl ox_reservar
  str x0, [x29, #64]
  str x0, [x29, #72]
  str xzr, [x29, #48]
  ldr x9, [x29, #40]
  cbz x9, split_ultimo

split_partir:
  ldp x0, x1, [x29, #16]
  ldp x2, x3, [x29, #32]
  ldr x4, [x29, #48]
  bl ox_buscar_texto
  tbnz x0, #63, split_ultimo
  // Celda {texto + posición, aparición - posición}
  ldr x9, [x29, #48]
  ldr x10, [x29, #16]
  add x10, x10, x9
  sub x11, x0, x9
  ldr x12, [x29, #72]
  stp x10, x11, [x12], #TAMANIO_CELDA
  str x12, [x29, #72]
  ldr x13, [x29, #40]
  add x0, x0, x13
  str x0, [x29, #48]
    b split_partir

split_ultimo:
  ldr x9, [x29, #48]
  ldp x10, x11, [x29, #16]
  add x10, x10, x9
  sub x11, x11, x9
  ldr x12, [x29, #72]
  stp x10, x11, [x12]

  ldr x0, [x29, #64]
  ldr x1, [x29, #56]
  ldp x29, x30, [sp], #80
  ret
