// ox_print_array(x0 = puntero a la primera celda, x1 = cantidad, x2 = descriptor)
// Escribe [e1, e2, ...]. El arreglo es un bloque plano en row-major: un
// [[i32; 3]; 2] son 6 celdas seguidas. El descriptor es una lista en .rodata:
//   .quad manejador, celdas_por_elemento, longitud_del_elemento, <descriptor del elemento>
// Con celdas_por_elemento = 0 el elemento es una celda (escalar o String) y el manejador recibe
// x0 = celda+0 y x1 = celda+8. Si no, el elemento es un subarreglo plano: el manejador es
// ox_print_array y recibe x0 = dirección del subarreglo, x1 = su longitud y x2 = el resto.
//   [i32; 3]       -> .quad ox_print_i32, 0, 0
//   [[i32; 3]; 2]  -> .quad ox_print_array, 3, 3, ox_print_i32, 0, 0
// Usa x19-x24 y los guarda, porque deben sobrevivir a la llamada al manejador.
.global ox_print_array
.include "var_globs.s"

.section .rodata
texto_corchete_abre: .ascii "["
  .equ texto_corchete_abre_len, .-texto_corchete_abre
texto_corchete_cierra: .ascii "]"
  .equ texto_corchete_cierra_len, .-texto_corchete_cierra
texto_separador: .ascii ", "
  .equ texto_separador_len, .-texto_separador

.section .text
ox_print_array:
  stp x29, x30, [sp, #-64]!
  mov x29, sp
  stp x19, x20, [x29, #16]
  stp x21, x22, [x29, #32]
  stp x23, x24, [x29, #48]

  mov x19, x0                         // x19 = elemento actual
  mov x20, x1                         // x20 = elementos restantes
  ldr x22, [x2]                       // x22 = manejador del elemento
  ldr x23, [x2, #8]                   // x23 = celdas por elemento (0 = una celda)
  ldr x24, [x2, #16]                  // x24 = longitud del subarreglo
  add x21, x2, #24                    // x21 = descriptor del elemento

  ldr x0, =texto_corchete_abre
  mov x1, texto_corchete_abre_len
  bl ox_print
  cbz x20, arreglo_cerrar

arreglo_elemento:
  cbnz x23, arreglo_subarreglo
  ldp x0, x1, [x19], #TAMANIO_CELDA
    b arreglo_llamar

arreglo_subarreglo:
  mov x0, x19
  mov x1, x24
  add x19, x19, x23, lsl #4           // avanzar celdas_por_elemento * 16 bytes

arreglo_llamar:
  mov x2, x21
  blr x22
  subs x20, x20, #1
    b.eq arreglo_cerrar
  ldr x0, =texto_separador
  mov x1, texto_separador_len
  bl ox_print
    b arreglo_elemento

arreglo_cerrar:
  ldr x0, =texto_corchete_cierra
  mov x1, texto_corchete_cierra_len
  bl ox_print

  ldp x23, x24, [x29, #48]
  ldp x21, x22, [x29, #32]
  ldp x19, x20, [x29, #16]
  ldp x29, x30, [sp], #64
  ret
