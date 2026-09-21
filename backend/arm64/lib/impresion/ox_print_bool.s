# Recibe x0, 0 para false y 1 para true
.global ox_print_bool
.include "var_globs.s"

.section .rodata
texto_true: .ascii "true"
  .equ texto_true_len, .-texto_true
texto_false: .ascii "false"
  .equ texto_false_len, .-texto_false

.section .text
ox_print_bool:
  cbz x0, booleano_falso
  ldr x0, =texto_true
  mov x1, texto_true_len
    b ox_print

booleano_falso:
  ldr x0, =texto_false
  mov x1, texto_false_len
    b ox_print
