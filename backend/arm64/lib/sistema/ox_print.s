// Entran:
// x0 como puntero
// x1 longitud del texto
.global ox_print
.include "var_globs.s"

.section .text
ox_print:
  mov x2, x1
  mov x1, x0
  mov x0, STDOUT
  mov x8, WRITE
  svc #0
  ret
