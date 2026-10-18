import { elemento, escapar } from '../html';
import { vacio } from './pestanas';

// AST en Graphviz, servido por la API en /api/ast/<archivo>
export function mostrarAst(imagen: string | null) {
  const seccion = elemento('reporte-ast');
  if (!imagen) {
    seccion.innerHTML = vacio('No se generó el AST.');
    return;
  }
  const url = `/api/ast/${encodeURIComponent(imagen)}`;
  seccion.innerHTML = `<a class="reporte-enlace" href="${url}" target="_blank" rel="noopener">Abrir la imagen
    (${escapar(imagen)})</a><div class="reporte-ast"><img src="${url}" alt="AST del programa" /></div>`;
}
