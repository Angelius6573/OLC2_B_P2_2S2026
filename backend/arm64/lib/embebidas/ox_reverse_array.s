// ox_reverse_array(x0 = puntero, x1 = cantidad, x2 = celdas por elemento)
//   -> x0 y x1 sin cambios: el mismo arreglo, invertido en sitio
// Invierte los elementos de la dimensión exterior. En un arreglo plano de filas, cada fila
// ocupa celdas_por_elemento * 16 bytes y se intercambia entera.
.global ox_reverse_array

.section .text
ox_reverse_array:
  cmp x1, #1
    b.ls invertir_arreglo_fin
  lsl x3, x2, #4                  // x3 = bytes por elemento
  mov x9, x0                      // x9 = elemento izquierdo
  sub x10, x1, #1
  madd x10, x10, x3, x0           // x10 = elemento derecho

invertir_arreglo_par:
  cmp x9, x10
    b.hs invertir_arreglo_fin
  mov x11, #0

invertir_arreglo_palabra:
  ldr x12, [x9, x11]
  ldr x13, [x10, x11]
  str x13, [x9, x11]
  str x12, [x10, x11]
  add x11, x11, #8
  cmp x11, x3
    b.lo invertir_arreglo_palabra
  add x9, x9, x3
  sub x10, x10, x3
    b invertir_arreglo_par

invertir_arreglo_fin:
  ret
