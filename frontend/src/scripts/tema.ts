import { elemento } from './html';

const oyentes: ((oscuro: boolean) => void)[] = [];

export function esOscuro() {
  return document.documentElement.classList.contains('dark');
}

export function alCambiarTema(oyente: (oscuro: boolean) => void) {
  oyentes.push(oyente);
}

export function iniciarTema() {
  const boton = elemento('theme-toggle');
  boton.textContent = esOscuro() ? 'Oscuro' : 'Claro';
  boton.addEventListener('click', () => {
    const oscuro = !esOscuro();
    document.documentElement.classList.toggle('dark', oscuro);
    try { localStorage.setItem('theme', oscuro ? 'dark' : 'light'); } catch {}
    boton.textContent = oscuro ? 'Oscuro' : 'Claro';
    oyentes.forEach(oyente => oyente(oscuro));
  });
}
