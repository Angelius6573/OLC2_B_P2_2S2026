// ox_print_char(x0 = punto de código Unicode): lo codifica en UTF-8 y lo escribe.
.global ox_print_char
.include "var_globs.s"

.section .text
ox_print_char:
  stp x29, x30, [sp, #-32]!
  mov x29, sp
  add x9, x29, #16          // buffer de 4 bytes

  cmp x0, #0x80
    b.lo caracter_1_byte
  cmp x0, #0x800
    b.lo caracter_2_bytes
  mov x10, #0x10000
  cmp x0, x10
    b.lo caracter_3_bytes

// 4 bytes: 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
  lsr x10, x0, #18
  orr x10, x10, #0xF0
  strb w10, [x9]
  ubfx x10, x0, #12, #6
  orr x10, x10, #0x80
  strb w10, [x9, #1]
  ubfx x10, x0, #6, #6
  orr x10, x10, #0x80
  strb w10, [x9, #2]
  and x10, x0, #0x3F
  orr x10, x10, #0x80
  strb w10, [x9, #3]
  mov x1, #4
    b caracter_escribir

// 3 bytes: 1110xxxx 10xxxxxx 10xxxxxx
caracter_3_bytes:
  lsr x10, x0, #12
  orr x10, x10, #0xE0
  strb w10, [x9]
  ubfx x10, x0, #6, #6
  orr x10, x10, #0x80
  strb w10, [x9, #1]
  and x10, x0, #0x3F
  orr x10, x10, #0x80
  strb w10, [x9, #2]
  mov x1, #3
    b caracter_escribir

// 2 bytes: 110xxxxx 10xxxxxx
caracter_2_bytes:
  lsr x10, x0, #6
  orr x10, x10, #0xC0
  strb w10, [x9]
  and x10, x0, #0x3F
  orr x10, x10, #0x80
  strb w10, [x9, #1]
  mov x1, #2
    b caracter_escribir

caracter_1_byte:
  strb w0, [x9]
  mov x1, #1

caracter_escribir:
  mov x0, x9
  bl ox_print

  ldp x29, x30, [sp], #32
  ret
