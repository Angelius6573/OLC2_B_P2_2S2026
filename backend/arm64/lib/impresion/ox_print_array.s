# ox_print_array(x0 = puntero a la primera celda, x1 = cantidad, x2 = descriptor)
# Escribe [e1, e2, ...]. El descriptor es una lista de punteros en .rodata:
# [manejador del elemento, resto]. Si el elemento es otro arreglo, su manejador es
# ox_print_array y recibe el resto como descriptor.
#   [i32]     -> .quad ox_print_i32
#   [[i32]]   -> .quad ox_print_array, ox_print_i32
#   [String]  -> .quad ox_print_string_debug
# Cada manejador recibe x0 = celda+0, x1 = celda+8 y x2 = descriptor del elemento.
# Usa x19-x22 y los guarda, porque deben sobrevivir a la llamada al manejador.
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
  stp x29, x30, [sp, #-48]!
  mov x29, sp
  stp x19, x20, [x29, #16]
  stp x21, x22, [x29, #32]

  mov x19, x0                         # x19 = celda actual
  mov x20, x1                         # x20 = celdas restantes
  ldr x22, [x2]                       # x22 = manejador del elemento
  add x21, x2, #8                     # x21 = descriptor del elemento

  ldr x0, =texto_corchete_abre
  mov x1, texto_corchete_abre_len
  bl ox_print
  cbz x20, arreglo_cerrar

arreglo_elemento:
  ldp x0, x1, [x19], #TAMANIO_CELDA
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

  ldp x21, x22, [x29, #32]
  ldp x19, x20, [x29, #16]
  ldp x29, x30, [sp], #48
  ret
