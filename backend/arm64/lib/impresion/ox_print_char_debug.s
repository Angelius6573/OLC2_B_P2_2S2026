// ox_print_char_debug(x0 = punto de código): escribe el carácter entre comillas simples ({:?}),
// como Rust: 'a'.
.global ox_print_char_debug

.section .rodata
texto_comilla_simple: .ascii "'"
  .equ texto_comilla_simple_len, .-texto_comilla_simple

.section .text
ox_print_char_debug:
  stp x29, x30, [sp, #-32]!
  mov x29, sp
  str x0, [x29, #16]

  ldr x0, =texto_comilla_simple
  mov x1, texto_comilla_simple_len
  bl ox_print
  ldr x0, [x29, #16]
  bl ox_print_char
  ldr x0, =texto_comilla_simple
  mov x1, texto_comilla_simple_len
  bl ox_print

  ldp x29, x30, [sp], #32
  ret
