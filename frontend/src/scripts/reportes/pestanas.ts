export type Pestana = 'errores' | 'simbolos' | 'ast' | 'tokens';

export function activarPestana(pestana: Pestana) {
  document.querySelectorAll<HTMLElement>('.pestana').forEach(boton =>
    boton.classList.toggle('activa', boton.dataset.pestana === pestana));
  document.querySelectorAll<HTMLElement>('.reporte').forEach(seccion =>
    seccion.classList.toggle('activo', seccion.id === `reporte-${pestana}`));
}

export function iniciarPestanas() {
  document.querySelectorAll<HTMLElement>('.pestana').forEach(boton =>
    boton.addEventListener('click', () => activarPestana(boton.dataset.pestana as Pestana)));
}

export function vacio(mensaje: string) {
  return `<p class="ide-vacio">${mensaje}</p>`;
}
