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

// Estado, tiempos, salida del programa y, debajo, cada error con el formato del enunciado
export function mostrarConsola(respuesta: RespuestaCompilacion) {
  const { status, output, errors } = respuesta;
  let html = `<p class="consola-estado ${status.ok ? 'ok' : 'error'}">${escapar(status.message)}</p>`;
  html += tiempos(respuesta);
  html += output
    ? `<pre class="consola-salida">${escapar(output)}</pre>`
    : '<p class="ide-vacio" style="text-align: left; padding: 0;">Sin salida.</p>';
  if (errors.length) {
    html += `<pre class="consola-errores">${escapar(errors.map(e => e.texto).join('\n\n'))}</pre>`;
  }
  elemento('consola').innerHTML = html;
}
