import type { RespuestaCompilacion } from './api';
import type { Editor } from './editor';
import { descargar, elemento } from './html';

let asm = '';

export function iniciarArm64(visor: Editor) {
  elemento('btn-descargar-asm').addEventListener('click', () => descargar('programa.s', asm));
  return (respuesta: RespuestaCompilacion | null) => mostrarArm64(visor, respuesta);
}

function mostrarArm64(visor: Editor, respuesta: RespuestaCompilacion | null) {
  const bloque = respuesta?.arm64 ?? null;
  const aviso = elemento('aviso-arm64');
  asm = bloque?.asm ?? '';
  visor.fijar(asm);
  (elemento('btn-descargar-asm') as HTMLButtonElement).disabled = !asm;

  let texto = '';
  if (bloque?.notice) texto = bloque.notice;
  else if (respuesta?.mode === 'interprete') texto = 'Modo intérprete: no se genera código ARM64.';
  else if (respuesta && !bloque) texto = 'No se generó código: el programa tiene errores.';
  aviso.textContent = texto;
  aviso.hidden = !texto;
}
