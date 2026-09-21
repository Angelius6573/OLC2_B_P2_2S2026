.global ox_print_nl
.include "var_globs.s"

.section .rodata
texto_salto: .ascii "\n"
  .equ texto_salto_len, .-texto_salto

.section .text
ox_print_nl:
  ldr x0, =texto_salto
  mov x1, texto_salto_len
    b ox_print
