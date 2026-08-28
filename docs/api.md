# Referencia de la API REST — OxigenScript

**Volver al índice:** [Documentación técnica](DOCUMENTACION_TECNICA.md)

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/compile` | Compila y ejecuta; devuelve `{output, errors, symbols, ast_image}` |
| `POST` | `/api/tokens` | Devuelve `{tokens: [{type, lexema, value, line, col}]}` |
| `GET` | `/api/ast/{filename}` | Sirve el PNG del AST |

El backend es una aplicación **FastAPI** lanzada con **Uvicorn** en el puerto `8000`. El frontend (Astro, puerto `4321`) consume estos endpoints a través de `api/compiler.py` y `api/tokens.py`.
