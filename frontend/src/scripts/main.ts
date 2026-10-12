import { compilar, obtenerTokens, type Modo, type RespuestaCompilacion } from './api';
import { iniciarArchivo } from './archivo';
import { iniciarArm64 } from './arm64';
import { limpiarConsola, mostrarConsola, mostrarEjecutando, mostrarFallo } from './consola';
import { crearEditorFuente, crearVisor } from './editor';
import { elemento } from './html';
import { mostrarAst } from './reportes/ast';
import { mostrarErrores } from './reportes/errores';
import { iniciarMenuReportes } from './reportes/menu';
import { activarPestana, iniciarPestanas, vacio } from './reportes/pestanas';
import { mostrarSimbolos } from './reportes/simbolos';
import { mostrarTokens } from './reportes/tokens';
import { iniciarTema } from './tema';

const CLAVE_CODIGO = 'oxigen_code';
const CLAVE_MODO = 'oxigen_mode';
const EJEMPLO = 'fn main() {\n    println!("Hola OxigenNative!");\n}\n';

function leer(clave: string) {
  try { return localStorage.getItem(clave); } catch { return null; }
}

function guardar(clave: string, valor: string) {
  try { localStorage.setItem(clave, valor); } catch {}
}

let ultima: RespuestaCompilacion | null = null;

iniciarTema();
iniciarPestanas();

const selectorModo = elemento('selector-modo') as HTMLSelectElement;
selectorModo.value = leer(CLAVE_MODO) === 'interprete' ? 'interprete' : 'arm64';
selectorModo.addEventListener('change', () => guardar(CLAVE_MODO, selectorModo.value));

const editor = crearEditorFuente(elemento('contenedor-editor'), leer(CLAVE_CODIGO) ?? EJEMPLO,
  texto => guardar(CLAVE_CODIGO, texto), ejecutar);
const mostrarArm64 = iniciarArm64(crearVisor(elemento('contenedor-arm64')));

iniciarArchivo(editor, limpiarResultados);
iniciarMenuReportes(() => ultima?.symbols_report ?? null);
elemento('btn-ejecutar').addEventListener('click', ejecutar);

function limpiarResultados() {
  ultima = null;
  limpiarConsola();
  mostrarArm64(null);
  document.querySelectorAll('.reporte').forEach(seccion => {
    seccion.innerHTML = vacio('Ejecuta un programa para ver este reporte.');
  });
}

async function ejecutar() {
  const codigo = editor.texto();
  if (!codigo.trim()) return;
  const boton = elemento('btn-ejecutar') as HTMLButtonElement;
  boton.disabled = true;
  boton.textContent = 'Ejecutando…';
  mostrarEjecutando();
  try {
    const [respuesta, tokens] = await Promise.all([
      compilar(codigo, selectorModo.value as Modo), obtenerTokens(codigo),
    ]);
    ultima = respuesta;
    mostrarConsola(respuesta);
    mostrarArm64(respuesta);
    mostrarErrores(respuesta.errors, editor.irA);
    mostrarSimbolos(respuesta.symbols, respuesta.symbols_report);
    mostrarAst(respuesta.ast_image);
    mostrarTokens(tokens);
    if (respuesta.errors.length) activarPestana('errores');
  } catch (error) {
    mostrarFallo(`No se pudo contactar al servidor: ${error}`);
  } finally {
    boton.disabled = false;
    boton.textContent = 'Ejecutar';
  }
}
