// Recibe x6, registro de error propio, ejecuta la impresión del tipo de error de la siguiente forma
//   [Ejecucion] Línea L, Columna C: mensaje
// y devuelve el control.
// Todos estos son básicamente errores semanticos o que en caso de que no haya
// salvaguarda va a joder el sistema
.global ox_error
.include "var_globs.s"

.section .rodata
  error_prefijo: .ascii "[Ejecucion] Línea "
    .equ error_prefijo_len, .-error_prefijo
  error_columna: .ascii ", Columna "
    .equ error_columna_len, .-error_columna
  error_dos_puntos: .ascii ": "
    .equ error_dos_puntos_len, .-error_dos_puntos
  error_salto: .ascii "\n"
    .equ error_salto_len, .-error_salto
  mensaje_desconocido: .ascii "Error de ejecución desconocido."
    .equ mensaje_desconocido_len, .-mensaje_desconocido
  mensaje_indice_fuera: .ascii "Índice fuera de los límites del arreglo."
    .equ mensaje_indice_fuera_len, .-mensaje_indice_fuera
  mensaje_division_cero: .ascii "División por cero."
    .equ mensaje_division_cero_len, .-mensaje_division_cero
  mensaje_modulo_cero: .ascii "Módulo por cero."
    .equ mensaje_modulo_cero_len, .-mensaje_modulo_cero
  mensaje_sin_memoria: .ascii "Memoria del heap agotada."
    .equ mensaje_sin_memoria_len, .-mensaje_sin_memoria

  // La entrada 0 cubre cualquier código fuera de rango.
  .align 3
  tabla_errores:
    .quad mensaje_desconocido, mensaje_desconocido_len
    .quad mensaje_indice_fuera, mensaje_indice_fuera_len
    .quad mensaje_division_cero, mensaje_division_cero_len
    .quad mensaje_modulo_cero, mensaje_modulo_cero_len
    .quad mensaje_sin_memoria, mensaje_sin_memoria_len

.section .text
ox_error:
  stp x29, x30, [sp, #-80]!
  mov x29, sp
  stp x0, x1, [x29, #16]        // línea, columna
  str x6, [x29, #32]            // código

  ldr x0, =error_prefijo
  mov x1, error_prefijo_len
  bl ox_print_err
  ldr x0, [x29, #16]
  add x1, x29, #48              // buffer de 32 bytes
  bl ox_int_to_str
  bl ox_print_err

  ldr x0, =error_columna
  mov x1, error_columna_len
  bl ox_print_err
  ldr x0, [x29, #24]
  add x1, x29, #48
  bl ox_int_to_str
  bl ox_print_err

  ldr x0, =error_dos_puntos
  mov x1, error_dos_puntos_len
  bl ox_print_err

  // Un código fuera de 1..ERR_ULTIMO usa la entrada 0. La comparación sin signo cubre los negativos
  ldr x9, [x29, #32]
  cmp x9, ERR_ULTIMO
    b.ls error_conocido
  mov x9, #0

error_conocido:
  ldr x10, =tabla_errores
  add x10, x10, x9, lsl #4
  ldp x0, x1, [x10]
  bl ox_print_err

  ldr x0, =error_salto
  mov x1, error_salto_len
  bl ox_print_err

  ldp x29, x30, [sp], #80
  ret
