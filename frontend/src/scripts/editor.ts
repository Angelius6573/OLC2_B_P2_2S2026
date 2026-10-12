import { EditorView, keymap, lineNumbers, highlightActiveLine, highlightActiveLineGutter } from '@codemirror/view';
import { Compartment, EditorState, type Extension } from '@codemirror/state';
import { defaultKeymap, history, historyKeymap } from '@codemirror/commands';
import { javascript } from '@codemirror/lang-javascript';
import { oneDark } from '@codemirror/theme-one-dark';
import { syntaxHighlighting, defaultHighlightStyle, bracketMatching, foldGutter, indentOnInput } from '@codemirror/language';
import { closeBrackets, closeBracketsKeymap } from '@codemirror/autocomplete';
import { highlightSelectionMatches, searchKeymap } from '@codemirror/search';
import { alCambiarTema, esOscuro } from './tema';

const temaClaro = EditorView.theme({
  '&': { backgroundColor: '#ffffff', color: '#1a1028' },
  '.cm-content': { caretColor: '#7c3aed', fontFamily: "'Fira Code',monospace", fontSize: '14px' },
  '.cm-cursor': { borderLeftColor: '#7c3aed' },
  '.cm-activeLine': { backgroundColor: '#f0eaf8' },
  '.cm-activeLineGutter': { backgroundColor: '#f0eaf8' },
  '.cm-gutters': { backgroundColor: '#f8f7fc', color: '#9580ab', border: 'none', borderRight: '1px solid #e0d8f0' },
  '.cm-selectionBackground': { backgroundColor: '#e0d0f5 !important' },
});

export interface Editor {
  texto(): string;
  fijar(texto: string): void;
  irA(linea: number, columna: number): void;
}

function crear(contenedor: HTMLElement, documento: string, extensiones: Extension[]): Editor {
  const tema = new Compartment();
  const vista = new EditorView({
    state: EditorState.create({
      doc: documento,
      extensions: [...extensiones, tema.of(esOscuro() ? oneDark : temaClaro)],
    }),
    parent: contenedor,
  });
  alCambiarTema(oscuro => vista.dispatch({ effects: tema.reconfigure(oscuro ? oneDark : temaClaro) }));
  return {
    texto: () => vista.state.doc.toString(),
    fijar: texto => vista.dispatch({ changes: { from: 0, to: vista.state.doc.length, insert: texto } }),
    // Línea y columna desde 1, como las reporta el compilador
    irA: (linea, columna) => {
      const documento = vista.state.doc;
      if (linea < 1 || linea > documento.lines) return;
      const destino = documento.line(linea);
      const posicion = Math.min(destino.from + Math.max(columna - 1, 0), destino.to);
      vista.dispatch({ selection: { anchor: posicion }, scrollIntoView: true });
      vista.focus();
    },
  };
}

// Editor de código fuente con numeración de líneas (enunciado §3.1.2)
export function crearEditorFuente(contenedor: HTMLElement, documento: string,
                                  alCambiar: (texto: string) => void, alEjecutar: () => void): Editor {
  return crear(contenedor, documento, [
    lineNumbers(), highlightActiveLineGutter(), history(), foldGutter(),
    // fallback: el resaltado de oneDark manda en tema oscuro; el por defecto solo cubre el claro
    indentOnInput(), syntaxHighlighting(defaultHighlightStyle, { fallback: true }), bracketMatching(),
    closeBrackets(), highlightActiveLine(), highlightSelectionMatches(),
    keymap.of([
      { key: 'Mod-Enter', run: () => { alEjecutar(); return true; } },
      ...closeBracketsKeymap, ...defaultKeymap, ...searchKeymap, ...historyKeymap,
    ]),
    javascript(), EditorView.lineWrapping,
    EditorView.updateListener.of(u => { if (u.docChanged) alCambiar(u.state.doc.toString()); }),
  ]);
}

// Visor de programa.s: solo lectura, con números de línea para ubicar los errores de `as`
export function crearVisor(contenedor: HTMLElement): Editor {
  return crear(contenedor, '', [
    lineNumbers(), highlightActiveLine(), EditorState.readOnly.of(true), EditorView.editable.of(false),
  ]);
}
