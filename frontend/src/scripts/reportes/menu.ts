import { elemento } from '../html';
import { activarPestana, type Pestana } from './pestanas';
import { urlReporteSimbolos } from './simbolos';

// Botón Reportes de la barra: lleva a una pestaña o abre el reporte HTML de símbolos
export function iniciarMenuReportes(reporteActual: () => string | null) {
  const boton = elemento('btn-reportes');
  const menu = elemento('menu-reportes');
  boton.addEventListener('click', evento => {
    evento.stopPropagation();
    menu.classList.toggle('abierto');
  });
  document.addEventListener('click', () => menu.classList.remove('abierto'));

  menu.querySelectorAll<HTMLElement>('[data-reporte]').forEach(opcion =>
    opcion.addEventListener('click', () => {
      const reporte = opcion.dataset.reporte!;
      if (reporte === 'simbolos-html') {
        const nombre = reporteActual();
        if (nombre) window.open(urlReporteSimbolos(nombre), '_blank', 'noopener');
        else alert('Ejecuta un programa para generar el reporte de símbolos.');
        return;
      }
      activarPestana(reporte as Pestana);
      elemento('panel-reportes').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }));
}
