.global ox_terminar
.include "var_globs.s"

.section .text
ox_terminar:
  mov x0, #0
  mov x8, EXIT
  svc #0
