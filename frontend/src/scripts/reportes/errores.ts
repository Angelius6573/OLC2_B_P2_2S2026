import type { ErrorCompilacion } from '../api';
import { elemento, escapar } from '../html';
import { vacio } from './pestanas';

// Categoría del mensaje "[Categoria] ..." -> texto y color de la columna Tipo
const TIPOS: Record<string, [string, string]> = {
  Lexico: ['Léxico', '#f59e0b'],
  Sintactico: ['Sintáctico', '#ef4444'],
  Semantico: ['Semántico', '#8b5cf6'],
  Ejecucion: ['Ejecución', '#ec4899'],
  Generacion: ['Generación', '#22d3ee'],
};

// Tabla de análisis de errores (enunciado §3.5.1): No, Tipo, Descripción, Línea, Columna
export function mostrarErrores(errores: ErrorCompilacion[]) {
  const seccion = elemento('reporte-errores');
  if (!errores.length) {
    seccion.innerHTML = vacio('Sin errores.');
    return;
  }
  const filas = errores.map((error, i) => {
    const categoria = error.message.match(/^\[(\w+)\]/)?.[1] ?? '';
    const [tipo, color] = TIPOS[categoria] ?? [categoria || 'Error', '#94a3b8'];
    const descripcion = error.message.replace(/^\[\w+\]\s*/, '');
    return `<tr><td>${i + 1}</td>
      <td><span class="etiqueta" style="background:${color}22;color:${color};">${escapar(tipo)}</span></td>
      <td>${escapar(descripcion)}</td><td>${error.line}</td><td>${error.col}</td></tr>`;
  }).join('');
  seccion.innerHTML = `<table><thead><tr><th>No</th><th>Tipo</th><th>Descripción</th>
    <th>Línea</th><th>Columna</th></tr></thead><tbody>${filas}</tbody></table>`;
}
