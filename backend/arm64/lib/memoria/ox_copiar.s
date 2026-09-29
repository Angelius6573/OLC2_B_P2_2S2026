// ox_copiar(x0 = destino, x1 = origen, x2 = bytes): copia byte a byte de origen a destino.
// No modifica x0, así que el llamador conserva la dirección de destino.
.global ox_copiar

.section .text
ox_copiar:
  cbz x2, copiar_fin
  mov x9, #0

copiar_byte:
  ldrb w10, [x1, x9]
  strb w10, [x0, x9]
  add x9, x9, #1
  cmp x9, x2
    b.lo copiar_byte

copiar_fin:
  ret
