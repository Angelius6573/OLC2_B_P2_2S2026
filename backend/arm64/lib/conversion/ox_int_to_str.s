# Entran:
# x0 inicio del texto
# x1 longitud del texto
.global ox_int_to_str
.include "var_globs.s"

.section .text
ox_int_to_str:
  mov x9, x1                # x9 = inicio del buffer
  mov x2, x1                # x2 = puntero de escritura
  mov x3, #10

  tbz x0, #63, entero_positivo
  mov w5, MINUS
  strb w5, [x2], #1
  neg x0, x0                # El mínimo de 64 bits se queda igual, pero udiv lo lee sin signo

entero_positivo:
  mov x10, x2               # x10 = primer dígito, después del signo
  cbnz x0, entero_convertir
  mov w5, ZERO
  strb w5, [x2], #1
    b entero_fin

entero_convertir:
  udiv x4, x0, x3           # x4 = x0 / 10
  msub x5, x4, x3, x0       # x5 = x0 - x4 * 10
  mov x0, x4
  add x5, x5, ZERO
  strb w5, [x2], #1
  cbnz x0, entero_convertir

  # Los dígitos quedaron del menos al más significativo: se invierten en sitio.
  mov x11, x10
  sub x12, x2, #1

entero_invertir:
  cmp x11, x12
    b.hs entero_fin
  ldrb w4, [x11]
  ldrb w5, [x12]
  strb w5, [x11], #1
  strb w4, [x12], #-1
    b entero_invertir

entero_fin:
  sub x1, x2, x9
  mov x0, x9
  ret
