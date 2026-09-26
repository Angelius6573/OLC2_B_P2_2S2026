.global ox_terminar
.include "var_globs.s"

.section .text
ox_terminar:
  mov x8, EXIT
  svc #0
