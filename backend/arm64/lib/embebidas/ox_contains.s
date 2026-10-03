// ox_contains(x0 = texto, x1 = longitud, x2 = patrón, x3 = longitud del patrón) -> x0 = bool
// El patrón vacío está contenido en cualquier texto.
.global ox_contains

.section .text
ox_contains:
  stp x29, x30, [sp, #-16]!
  mov x29, sp
  mov x4, #0
  bl ox_buscar_texto
  cmp x0, #0
  cset x0, ge
  ldp x29, x30, [sp], #16
  ret
