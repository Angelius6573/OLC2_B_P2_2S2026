# API REST

**Volver al índice:** [Documentación técnica](DOCUMENTACION_TECNICA.md)

El backend es una aplicación **FastAPI** (`api/main.py`) servida por **Uvicorn** en el puerto
`8000`. El frontend (Astro, puerto `4321`) reenvía `/api` a esa dirección.

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/compile` | Analiza, ejecuta en el modo pedido y devuelve salida, errores y reportes |
| `POST` | `/api/tokens` | Lista de tokens del código |
| `GET` | `/api/ast/{archivo}` | Imagen PNG del AST |
| `GET` | `/api/reportes/{archivo}` | Reporte HTML de la tabla de símbolos |

## `POST /api/compile`

Petición:

```json
{ "code": "fn main() { println!(\"Hola\"); }", "mode": "arm64" }
```

`mode` es `arm64` (por omisión) o `interprete`.

Respuesta:

| Campo | Contenido |
|---|---|
| `mode` | El modo pedido |
| `output` | Salida del programa (stdout) |
| `errors` | Tabla de errores: `{no, categoria, tipo, linea, columna, descripcion, fragmento, texto}` (ver [errores](errores.md)) |
| `symbols` | Tabla de símbolos: `{no, identificador, categoria, tipo, ambito, linea, valor, sym_id}` |
| `symbols_report` | Nombre del reporte HTML en `/api/reportes/` |
| `ast_image` | Nombre del PNG en `/api/ast/` |
| `arm64` | `null` en modo intérprete o si no se ejecutó; si no, `{asm, stage, success, exit_code, stderr, times, notice}` |
| `status` | Mensaje de la consola: `{ok, message, time_ms}` |

En el bloque `arm64`:

- `asm` es el `programa.s` generado. Va vacío si se ejecutó con el intérprete.
- `stage` es la última etapa alcanzada: `generacion`, `ensamblado`, `enlace` o `ejecucion`.
- `times` da los milisegundos de cada etapa (`generacion`, `construccion`, `ejecucion` o
  `interprete`).
- `notice` explica por qué se usó el intérprete: errores semánticos, o structs y slices.

Ejemplo, con el programa del [ejemplo de entrada y salida](arm64.md#8-ejemplo-de-entrada-y-salida):

```json
{
  "mode": "arm64",
  "output": "Resultado: 15\n",
  "errors": [],
  "arm64": { "stage": "ejecucion", "success": true, "exit_code": 0,
             "times": { "generacion": 0.4, "construccion": 5.0, "ejecucion": 7.5 }, "notice": null, "...": "..." },
  "status": { "ok": true, "message": "Compilación exitosa (ARM64). Ejecutado con QEMU en 7.5 ms.", "time_ms": 7.5 }
}
```

## `POST /api/tokens`

Petición `{ "code": "..." }`. Respuesta:
`{ "tokens": [{ "type", "lexema", "value", "line", "col" }] }`.

## Probar sin la GUI

```sh
curl -s localhost:8000/api/compile -H 'Content-Type: application/json' \
     -d '{"code": "fn main() { println!(\"Hola\"); }", "mode": "arm64"}'
```

O directamente desde Python, sin levantar el servidor:

```sh
.venv/bin/python -c "from api.compiler import compilar_codigo; r = compilar_codigo(open('programa.ox').read()); print(r['output']); print(r['errors'])"
```
