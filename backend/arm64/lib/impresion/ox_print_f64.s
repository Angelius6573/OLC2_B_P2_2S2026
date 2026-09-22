// ox_print_f64(x0 = bits IEEE-754 del f64):
//   0.0 y -0.0 -> "0.0". Sin decimales -> solo la parte entera ("2").
//   Con decimales -> hasta seis, redondeados, sin ceros a la derecha ("3.14").
// La parte entera se satura en el máximo de i64, pero eso no importa
.global ox_print_f64
.include "var_globs.s"

.section .rodata
texto_cero_f64: .ascii "0.0"
  .equ texto_cero_f64_len, .-texto_cero_f64

.section .text
ox_print_f64:
  stp x29, x30, [sp, #-64]!
  mov x29, sp

  fmov d0, x0
  fcmp d0, #0.0
    b.eq flotante_cero
  add x13, x29, #16         // x13 = puntero de escritura en el buffer de 48 bytes
    b.gt flotante_positivo
  mov w9, MINUS
  strb w9, [x13], #1
  fneg d0, d0

flotante_positivo:
  frintz d1, d0
  fcvtzs x14, d1            // x14 = parte entera
  fsub d2, d0, d1           // d2 = fracción en [0, 1)
  ldr x9, =UN_MILLON        // 0xF4240 no cabe en un solo mov
  ucvtf d3, x9
  fmul d2, d2, d3
  frinta d2, d2             // redondeo al más cercano; evita 2.675 -> 2.674999
  fcvtzs x15, d2            // x15 = fracción por 10^6
  cmp x15, x9
    b.lo flotante_sin_acarreo
  // 0.9999996 redondea a 1000000: la unidad pasa a la parte entera
  add x14, x14, #1
  mov x15, #0

flotante_sin_acarreo:
  // Un valor que redondea a cero en ambas partes, como -0.0000001, se escribe 0.0
  orr x9, x14, x15
  cbz x9, flotante_cero

  mov x0, x14
  mov x1, x13
  bl ox_int_to_str
  add x13, x0, x1
  cbz x15, flotante_escribir

  mov w9, PUNTO
  strb w9, [x13], #1

// Seis dígitos con ceros a la izquierda, escritos del último al primero.
  add x13, x13, DECIMALES_F64
  mov x10, x13
  mov x11, #10
  mov x3, DECIMALES_F64

flotante_digito:
  udiv x12, x15, x11
  msub x9, x12, x11, x15
  add x9, x9, ZERO
  strb w9, [x10, #-1]!
  mov x15, x12
  subs x3, x3, #1
    b.ne flotante_digito

// Quitar ceros a la derecha. La fracción no es cero, así que el bucle se detiene antes del punto.
flotante_quitar_ceros:
  ldrb w9, [x13, #-1]
  cmp w9, ZERO
    b.ne flotante_escribir
  sub x13, x13, #1
    b flotante_quitar_ceros

flotante_escribir:
  add x0, x29, #16
  sub x1, x13, x0
  bl ox_print
    b flotante_salir

flotante_cero:
  ldr x0, =texto_cero_f64
  mov x1, texto_cero_f64_len
  bl ox_print

flotante_salir:
  ldp x29, x30, [sp], #64
  ret
