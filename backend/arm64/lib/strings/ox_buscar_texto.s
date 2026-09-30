// ox_buscar_texto(x0 = texto, x1 = longitud, x2 = patrón, x3 = longitud del patrón, x4 = desde)
//   -> x0 = posición de la primera aparición del patrón en [desde, longitud), o -1
// Con el patrón vacío devuelve `desde`. Solo usa x0-x4 y x9-x14: no llama a nadie.
.global ox_buscar_texto

.section .text
ox_buscar_texto:
  mov x9, x4                      // x9 = posición candidata

buscar_candidato:
  add x10, x9, x3
  cmp x10, x1
    b.hi buscar_no_encontrado     // el patrón ya no cabe
  mov x11, #0                     // x11 = byte del patrón

buscar_byte:
  cmp x11, x3
    b.hs buscar_encontrado
  add x12, x9, x11
  ldrb w13, [x0, x12]
  ldrb w14, [x2, x11]
  cmp w13, w14
    b.ne buscar_siguiente
  add x11, x11, #1
    b buscar_byte

buscar_siguiente:
  add x9, x9, #1
    b buscar_candidato

buscar_encontrado:
  mov x0, x9
  ret

buscar_no_encontrado:
  mov x0, #-1
  ret
