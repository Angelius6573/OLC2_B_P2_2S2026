// ox_random(x0 = mínimo, x1 = máximo) -> x0 = entero aleatorio en [mínimo, máximo]
// Ambos extremos incluidos, como randint del intérprete; si vienen al revés se intercambian.
// xorshift64 con el estado en .bss. La semilla sale de getrandom en la primera llamada.
.global ox_random
.include "var_globs.s"

.section .bss
  .align 3
  estado_random: .skip 8

.section .text
ox_random:
  stp x29, x30, [sp, #-32]!
  mov x29, sp
  stp x0, x1, [x29, #16]

  ldr x9, =estado_random
  ldr x10, [x9]
  cbnz x10, random_siguiente
  mov x0, x9
  mov x1, #8
  mov x2, #0
  mov x8, GETRANDOM
  svc #0
  ldr x9, =estado_random
  ldr x10, [x9]
  cbnz x10, random_siguiente
  ldr x10, =0x9E3779B97F4A7C15    // xorshift no admite el estado 0

random_siguiente:
  eor x10, x10, x10, lsl #13
  eor x10, x10, x10, lsr #7
  eor x10, x10, x10, lsl #17
  str x10, [x9]

  ldp x0, x1, [x29, #16]
  cmp x0, x1
    b.le random_rango
  mov x11, x0
  mov x0, x1
  mov x1, x11

random_rango:
  sub x11, x1, x0
  add x11, x11, #1                // x11 = cantidad de valores posibles
  udiv x12, x10, x11
  msub x12, x12, x11, x10         // x12 = estado mod cantidad
  add x0, x0, x12

  ldp x29, x30, [sp], #32
  ret
