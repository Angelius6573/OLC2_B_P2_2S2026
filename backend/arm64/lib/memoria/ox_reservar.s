// ox_reservar(x0 = bytes) -> x0 = bloque alineado a 16 bytes, lleno de ceros.
// Bump allocator sin liberación. ptr_heap vale 0 hasta la primera
// reserva, que lo apunta al inicio de heap. Si el heap se agota, el error es crítico:
// se reporta y el programa termina con código 1.
.global ox_reservar
.include "var_globs.s"

.section .bss
  .align 4
  ptr_heap: .skip 8
  .align 4
  heap: .skip HEAP_TAMANIO
  heap_fin:

.section .text
ox_reservar:
  ldr x9, =ptr_heap
  ldr x10, [x9]
  cbnz x10, reservar_listo
  ldr x10, =heap

reservar_listo:
  add x0, x0, #15
  and x0, x0, #-16                // redondear al múltiplo de 16
  add x11, x10, x0                // x11 = nuevo tope
  ldr x12, =heap_fin
  cmp x11, x12
    b.hi reservar_sin_memoria
  str x11, [x9]
  mov x0, x10
  ret

reservar_sin_memoria:
  stp x29, x30, [sp, #-16]!
  mov x29, sp
  mov x6, ERR_SIN_MEMORIA
  mov x0, #0
  mov x1, #0
  bl ox_error
  mov x0, #1
    b ox_terminar
