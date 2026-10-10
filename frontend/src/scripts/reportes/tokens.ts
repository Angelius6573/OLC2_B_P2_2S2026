import type { Token } from '../api';
import { elemento, escapar } from '../html';
import { vacio } from './pestanas';

export function mostrarTokens(tokens: Token[]) {
  const seccion = elemento('reporte-tokens');
  if (!tokens.length) {
    seccion.innerHTML = vacio('No hay tokens.');
    return;
  }
  const filas = tokens.map((t, i) => `<tr><td>${i + 1}</td><td>${escapar(t.type)}</td>
    <td>${escapar(t.lexema)}</td><td class="mono">${escapar(t.value)}</td><td>${t.line}</td>
    <td>${t.col}</td></tr>`).join('');
  seccion.innerHTML = `<table><thead><tr><th>#</th><th>Tipo</th><th>Lexema</th><th>Valor</th>
    <th>Línea</th><th>Columna</th></tr></thead><tbody>${filas}</tbody></table>`;
}
