# Estructura de directorios — OxigenScript

**Volver al índice:** [Documentación técnica](DOCUMENTACION_TECNICA.md)

```
backend/
├── analizador_lexico.py        # Lexer PLY + 77 tokens
├── analizador_sintactico.py    # Parser PLY, precedencia, p_error
├── analizador_semantico.py     # Composición del checker (2 pasadas)
├── errores.py                  # reportar / limpiar / lista global
├── recorrer_ast.py             # Despacho por reflexión visitar_{Clase}
├── ast.py                      # Clase base Nodo (línea, columna)
├── sintax/                     # Reglas de gramática
├── ast_modular/                # Clases de nodos del AST
├── checker/                    # Tabla de símbolos + validación semántica
├── interpreter/                # Intérprete
└── visitor/grafo.py            # Generador del grafo del AST (PNG)

api/
├── main.py                     # FastAPI (puerto 8000)
├── compiler.py                 # Pipeline compilar_codigo
└── tokens.py                   # Endpoint de tokens

frontend/                       # IDE web (Astro, puerto 4321)
assets/ast/                     # PNGs del AST generados
docs/                           # Documentación y manual
```
