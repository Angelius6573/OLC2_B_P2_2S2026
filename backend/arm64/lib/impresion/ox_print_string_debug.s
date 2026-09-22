// ox_print_string_debug(x0 = puntero, x1 = longitud): escribe la cadena entre comillas
// dobles ({:?}).

.include "var_globs.s"

.global ox_print_string_debug

.section .rodata
texto_comilla: .ascii "\""
  .equ texto_comilla_len, .-texto_comilla

.section .text
ox_print_string_debug:
  stp x29, x30, [sp, #-32]!
  mov x29, sp
  stp x0, x1, [x29, #16]

  ldr x0, =texto_comilla
  mov x1, texto_comilla_len
  bl ox_print
  ldp x0, x1, [x29, #16]
  bl ox_print
  ldr x0, =texto_comilla
  mov x1, texto_comilla_len
  bl ox_print

  ldp x29, x30, [sp], #32
  ret
