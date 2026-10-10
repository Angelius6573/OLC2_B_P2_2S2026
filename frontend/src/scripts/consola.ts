import type { RespuestaCompilacion } from './api';
import { elemento, escapar } from './html';

const ETAPAS: Record<string, string> = {
  generacion: 'generación', construccion: 'as + ld', ejecucion: 'QEMU', interprete: 'intérprete',
};

function tiempos(respuesta: RespuestaCompilacion) {
  const veces = respuesta.arm64?.times;
  if (!veces) return '';
  const partes = Object.entries(veces).map(([etapa, ms]) => `${ETAPAS[etapa] ?? etapa} ${ms} ms`);
  return `<div class="ide-vacio" style="padding: 0 0 8px; text-align: left;">${escapar(partes.join(' · '))}</div>`;
}

export function mostrarEjecutando() {
  elemento('consola').innerHTML = '<p class="ide-vacio">Compilando y ejecutando…</p>';
}

export function mostrarFallo(mensaje: string) {
  elemento('consola').innerHTML = `<p class="consola-estado error">${escapar(mensaje)}</p>`;
}

export function limpiarConsola() {
  elemento('consola').innerHTML = '<p class="ide-vacio">Presiona «Ejecutar» para ver la salida.</p>';
}

// Estado, tiempos, salida del programa y errores de ejecución (lo que el programa escribe en stderr)
export function mostrarConsola(respuesta: RespuestaCompilacion) {
  const { status, output, errors } = respuesta;
  const deEjecucion = errors.filter(e => e.message.startsWith('[Ejecucion]'));
  let html = `<p class="consola-estado ${status.ok ? 'ok' : 'error'}">${escapar(status.message)}</p>`;
  html += tiempos(respuesta);
  html += output
    ? `<pre class="consola-salida">${escapar(output)}</pre>`
    : '<p class="ide-vacio" style="text-align: left; padding: 0;">Sin salida.</p>';
  if (deEjecucion.length) {
    const lineas = deEjecucion.map(e => e.line
      ? `${e.message.replace('[Ejecucion] ', `[Ejecucion] Línea ${e.line}, Columna ${e.col}: `)}`
      : e.message);
    html += `<pre class="consola-errores">${escapar(lineas.join('\n'))}</pre>`;
  }
  elemento('consola').innerHTML = html;
}
