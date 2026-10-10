const ENTIDADES: Record<string, string> = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };

// Todo texto que viene del programa o del compilador pasa por aquí antes de ir a innerHTML
export function escapar(texto: unknown): string {
  return String(texto).replace(/[&<>"']/g, c => ENTIDADES[c]);
}

export function elemento(id: string): HTMLElement {
  const nodo = document.getElementById(id);
  if (!nodo) throw new Error(`Falta el elemento #${id}`);
  return nodo;
}

export function descargar(nombre: string, contenido: string) {
  const enlace = document.createElement('a');
  enlace.href = URL.createObjectURL(new Blob([contenido], { type: 'text/plain' }));
  enlace.download = nombre;
  enlace.click();
  URL.revokeObjectURL(enlace.href);
}
