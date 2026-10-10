import type { Simbolo } from '../api';
import { elemento, escapar } from '../html';
import { vacio } from './pestanas';

export function urlReporteSimbolos(nombre: string) {
  return `/api/reportes/${encodeURIComponent(nombre)}`;
}

// Tabla de símbolos (enunciado §3.5.2): No., Identificador, Categoría, Tipo, Ámbito, Línea, Valor
export function mostrarSimbolos(simbolos: Simbolo[], reporte: string | null) {
  const seccion = elemento('reporte-simbolos');
  if (!simbolos.length) {
    seccion.innerHTML = vacio('No hay símbolos registrados.');
    return;
  }
  const filas = simbolos.map(s => `<tr><td>${s.no}</td><td>${escapar(s.identificador)}</td>
    <td>${escapar(s.categoria)}</td><td class="mono">${escapar(s.tipo)}</td><td>${escapar(s.ambito)}</td>
    <td>${s.linea}</td><td class="mono">${escapar(s.valor)}</td></tr>`).join('');
  const enlace = reporte
    ? `<a class="reporte-enlace" href="${urlReporteSimbolos(reporte)}" target="_blank" rel="noopener">Abrir el reporte HTML</a>`
    : '';
  seccion.innerHTML = `${enlace}<table><thead><tr><th>No.</th><th>Identificador</th><th>Categoría</th>
    <th>Tipo</th><th>Ámbito</th><th>Línea</th><th>Valor</th></tr></thead><tbody>${filas}</tbody></table>`;
}
