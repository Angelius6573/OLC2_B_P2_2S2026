# Entran:
# x0 como puntero
# x1 longitud del texto
.global ox_print_err
.include "var_globs.s"

.section .text
ox_print_err:
  mov x2, x1
  mov x1, x0
  mov x0, STDERR
  mov x8, WRITE
  svc #0
  ret
