import type { ErrorCompilacion } from '../api';
import { elemento, escapar } from '../html';
import { vacio } from './pestanas';

const COLORES: Record<ErrorCompilacion['categoria'], string> = {
  Lexico: '#f59e0b',
  Sintactico: '#ef4444',
  Semantico: '#8b5cf6',
  Ejecucion: '#ec4899',
  Generacion: '#22d3ee',
};

// Tabla de análisis de errores (enunciado §3.5.1): No, Tipo, Descripción con su fragmento, Línea, Columna.
// Un clic en una fila con posición lleva el cursor del editor a esa línea y columna.
export function mostrarErrores(errores: ErrorCompilacion[], irA: (linea: number, columna: number) => void) {
  const seccion = elemento('reporte-errores');
  if (!errores.length) {
    seccion.innerHTML = vacio('Sin errores.');
    return;
  }
  const filas = errores.map(error => {
    const color = COLORES[error.categoria] ?? '#94a3b8';
    const fragmento = error.fragmento ? `<pre class="fragmento">${escapar(error.fragmento)}</pre>` : '';
    const posicion = error.linea > 0
      ? ` class="con-posicion" data-linea="${error.linea}" data-columna="${error.columna}" title="Ir a la línea ${error.linea}"`
      : '';
    return `<tr${posicion}><td>${error.no}</td>
      <td><span class="etiqueta" style="background:${color}22;color:${color};">${escapar(error.tipo)}</span></td>
      <td>${escapar(error.descripcion)}${fragmento}</td>
      <td>${error.linea || '—'}</td><td>${error.linea ? error.columna : '—'}</td></tr>`;
  }).join('');
  seccion.innerHTML = `<table><thead><tr><th>No</th><th>Tipo</th><th>Descripción</th>
    <th>Línea</th><th>Columna</th></tr></thead><tbody>${filas}</tbody></table>`;
  seccion.querySelectorAll<HTMLElement>('tr.con-posicion').forEach(fila =>
    fila.addEventListener('click', () => irA(Number(fila.dataset.linea), Number(fila.dataset.columna))));
}
