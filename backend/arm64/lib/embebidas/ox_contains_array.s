// ox_contains_array(x0 = primera celda, x1 = cantidad, x2 = valor) -> x0 = bool
// Recorre las celdas de 16 bytes y compara su primera palabra con el valor (i32, bool, char).
.global ox_contains_array
.include "var_globs.s"

.section .text
ox_contains_array:
  cbz x1, arreglo_no_contiene

arreglo_comparar:
  ldr x9, [x0], #TAMANIO_CELDA
  cmp x9, x2
    b.eq arreglo_contiene
  subs x1, x1, #1
    b.ne arreglo_comparar

arreglo_no_contiene:
  mov x0, #0
  ret

arreglo_contiene:
  mov x0, #1
  ret
