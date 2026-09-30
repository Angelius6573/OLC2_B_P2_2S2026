// ox_concatenar(x0 = puntero 1, x1 = longitud 1, x2 = puntero 2, x3 = longitud 2)
//   -> x0 = bloque nuevo con los dos textos seguidos, x1 = longitud 1 + longitud 2
// Los textos de entrada no se modifican. Lo usan `+` entre String y push_str.
.global ox_concatenar

.section .text
ox_concatenar:
  stp x29, x30, [sp, #-64]!
  mov x29, sp
  stp x0, x1, [x29, #16]          // texto 1
  stp x2, x3, [x29, #32]          // texto 2

  add x0, x1, x3
  bl ox_reservar
  str x0, [x29, #48]              // bloque nuevo

  ldp x1, x2, [x29, #16]
  bl ox_copiar                    // texto 1 al inicio del bloque

  ldr x0, [x29, #48]
  ldr x9, [x29, #24]
  add x0, x0, x9
  ldp x1, x2, [x29, #32]
  bl ox_copiar                    // texto 2 detrás del texto 1

  ldr x0, [x29, #48]
  ldr x1, [x29, #24]
  ldr x9, [x29, #40]
  add x1, x1, x9

  ldp x29, x30, [sp], #64
  ret
