// ox_repetir(x0 = puntero, x1 = longitud, x2 = veces)
//   -> x0 = bloque nuevo con el texto repetido, x1 = longitud * veces
// Nota del enunciado §3.3.5: 2 * "ab" = "abab". Con veces <= 0 el resultado es el texto vacío.
.global ox_repetir

.section .text
ox_repetir:
  stp x29, x30, [sp, #-64]!
  mov x29, sp
  cmp x2, #0
  csel x2, x2, xzr, gt
  stp x0, x1, [x29, #16]          // texto
  str x2, [x29, #32]              // veces que faltan

  mul x0, x1, x2
  str x0, [x29, #56]              // longitud total
  bl ox_reservar
  str x0, [x29, #40]              // bloque nuevo
  str x0, [x29, #48]              // cursor de escritura

repetir_copia:
  ldr x9, [x29, #32]
  cbz x9, repetir_fin
  sub x9, x9, #1
  str x9, [x29, #32]
  ldr x0, [x29, #48]
  ldp x1, x2, [x29, #16]
  bl ox_copiar
  ldr x0, [x29, #48]
  ldr x9, [x29, #24]
  add x0, x0, x9
  str x0, [x29, #48]
    b repetir_copia

repetir_fin:
  ldr x0, [x29, #40]
  ldr x1, [x29, #56]
  ldp x29, x30, [sp], #64
  ret
