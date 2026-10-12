// Contrato de POST /api/compile y /api/tokens (api/compiler.py)
export type Modo = 'arm64' | 'interprete';

// Fila de la tabla de errores (backend/reportes/errores.py). `texto` tiene el formato del enunciado §3.5.1
export interface ErrorCompilacion {
  no: number;
  categoria: 'Lexico' | 'Sintactico' | 'Semantico' | 'Ejecucion' | 'Generacion';
  tipo: string;
  linea: number;
  columna: number;
  descripcion: string;
  fragmento: string | null;
  texto: string;
}

export interface Simbolo {
  no: number; identificador: string; categoria: string; tipo: string;
  ambito: string; linea: number; valor: string;
}

export interface BloqueArm64 {
  asm: string;
  stage: 'generacion' | 'ensamblado' | 'enlace' | 'ejecucion';
  success: boolean;
  exit_code: number | null;
  stderr: string;
  times: Record<string, number>;
  notice: string | null;
}

export interface Estado { ok: boolean; message: string; time_ms: number | null; }

export interface RespuestaCompilacion {
  mode: Modo;
  output: string;
  errors: ErrorCompilacion[];
  symbols: Simbolo[];
  symbols_report: string | null;
  ast_image: string | null;
  arm64: BloqueArm64 | null;
  status: Estado;
}

export interface Token { type: string; lexema: string; value: string; line: number; col: number; }

async function publicar<T>(ruta: string, cuerpo: object): Promise<T> {
  const respuesta = await fetch(ruta, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(cuerpo),
  });
  if (!respuesta.ok) throw new Error(`${ruta} respondió ${respuesta.status}`);
  return respuesta.json();
}

export function compilar(code: string, mode: Modo) {
  return publicar<RespuestaCompilacion>('/api/compile', { code, mode });
}

export async function obtenerTokens(code: string) {
  return (await publicar<{ tokens: Token[] }>('/api/tokens', { code })).tokens;
}
