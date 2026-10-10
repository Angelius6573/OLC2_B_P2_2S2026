import type { Editor } from './editor';
import { descargar, elemento } from './html';

const NOMBRE_POR_DEFECTO = 'programa.ox';
let nombre = NOMBRE_POR_DEFECTO;

function mostrarNombre() {
  elemento('nombre-archivo').textContent = `· ${nombre}`;
}

// Nuevo, Abrir y Guardar (enunciado §3.1.2). Abrir lee un .ox del disco y lo carga en el editor
export function iniciarArchivo(editor: Editor, alNuevo: () => void) {
  const entrada = elemento('entrada-archivo') as HTMLInputElement;
  mostrarNombre();

  elemento('btn-nuevo').addEventListener('click', () => {
    if (editor.texto().trim() && !confirm('¿Descartar el código actual y empezar un archivo nuevo?')) return;
    nombre = NOMBRE_POR_DEFECTO;
    mostrarNombre();
    editor.fijar('');
    alNuevo();
  });

  elemento('btn-abrir').addEventListener('click', () => entrada.click());
  entrada.addEventListener('change', () => {
    const archivo = entrada.files?.[0];
    if (!archivo) return;
    const lector = new FileReader();
    lector.onload = () => {
      nombre = archivo.name;
      mostrarNombre();
      editor.fijar(String(lector.result));
      alNuevo();
    };
    lector.readAsText(archivo);
    entrada.value = '';
  });

  elemento('btn-guardar').addEventListener('click', () => descargar(nombre, editor.texto()));
}
