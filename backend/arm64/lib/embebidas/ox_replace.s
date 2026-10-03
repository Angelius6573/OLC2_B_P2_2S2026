// ox_replace(x0 = texto, x1 = longitud, x2 = buscado, x3 = longitud buscado,
//            x4 = reemplazo, x5 = longitud reemplazo) -> x0 = bloque nuevo, x1 = su longitud
// Reemplaza todas las apariciones sin solaparse, de izquierda a derecha. Con el buscado vacío
// devuelve el mismo texto. Dos pasadas: contar apariciones, reservar y copiar.
.global ox_replace

// Marco: texto 16, longitud 24, buscado 32, longitud buscado 40, reemplazo 48,
// longitud reemplazo 56, posición 64, longitud total 72, bloque 80, cursor 88, aparición 96
.section .text
ox_replace:
  cbnz x3, replace_inicio
  ret

replace_inicio:
  stp x29, x30, [sp, #-112]!
  mov x29, sp
  stp x0, x1, [x29, #16]
  stp x2, x3, [x29, #32]
  stp x4, x5, [x29, #48]
  str xzr, [x29, #64]
  str x1, [x29, #72]              // longitud total, se ajusta por aparición

replace_contar:
  ldp x0, x1, [x29, #16]
  ldp x2, x3, [x29, #32]
  ldr x4, [x29, #64]
  bl ox_buscar_texto
  tbnz x0, #63, replace_reservar  // -1: no hay más apariciones
  ldr x9, [x29, #72]
  ldr x10, [x29, #56]
  ldr x11, [x29, #40]
  add x9, x9, x10
  sub x9, x9, x11
  str x9, [x29, #72]
  add x0, x0, x11
  str x0, [x29, #64]
    b replace_contar

replace_reservar:
  ldr x0, [x29, #72]
  bl ox_reservar
  str x0, [x29, #80]
  str x0, [x29, #88]
  str xzr, [x29, #64]

replace_copiar:
  ldp x0, x1, [x29, #16]
  ldp x2, x3, [x29, #32]
  ldr x4, [x29, #64]
  bl ox_buscar_texto
  tbnz x0, #63, replace_resto
  str x0, [x29, #96]
  // Tramo entre la posición y la aparición
  ldr x9, [x29, #64]
  sub x2, x0, x9
  ldr x1, [x29, #16]
  add x1, x1, x9
  ldr x0, [x29, #88]
  bl ox_copiar
  ldr x9, [x29, #96]
  ldr x10, [x29, #64]
  sub x9, x9, x10
  add x0, x0, x9
  // Reemplazo
  ldp x1, x2, [x29, #48]
  bl ox_copiar
  ldr x9, [x29, #56]
  add x0, x0, x9
  str x0, [x29, #88]
  ldr x9, [x29, #96]
  ldr x10, [x29, #40]
  add x9, x9, x10
  str x9, [x29, #64]
    b replace_copiar

replace_resto:
  ldr x9, [x29, #64]
  ldr x1, [x29, #16]
  add x1, x1, x9
  ldr x2, [x29, #24]
  sub x2, x2, x9
  ldr x0, [x29, #88]
  bl ox_copiar

  ldr x0, [x29, #80]
  ldr x1, [x29, #72]
  ldp x29, x30, [sp], #112
  ret
