// ox_print_i32(x0 = entero): escribe los 32 bits bajos, con signo.

.include "var_globs.s"

.global ox_print_i32

.section .text
ox_print_i32:
  stp x29, x30, [sp, #-48]!
  mov x29, sp

  sxtw x0, w0
  add x1, x29, #16          // buffer de 32 bytes dentro del marco
  bl ox_int_to_str
  bl ox_print

  ldp x29, x30, [sp], #48
  ret
