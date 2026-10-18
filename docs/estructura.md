# Estructura de directorios

**Volver al índice:** [Documentación técnica](DOCUMENTACION_TECNICA.md)

```
OxigenNative/
├── api/                            # Capa de lógica y servicios (FastAPI, puerto 8000)
│   ├── main.py                     # Rutas: /api/compile, /api/tokens, /api/ast, /api/reportes
│   ├── compiler.py                 # compilar_codigo: orquesta análisis, ejecución y reportes
│   ├── modo_arm64.py               # Pipeline ARM64 y respaldo con el intérprete
│   ├── modo_interprete.py          # Ejecución con el intérprete (salida, errores, valores)
│   ├── estado.py                   # Mensaje de estado de la consola
│   └── tokens.py                   # Lista de tokens para la pestaña Tokens
│
├── backend/
│   ├── analizador_lexico.py        # Lexer PLY: 77 tokens, comentarios, errores léxicos
│   ├── analizador_sintactico.py    # Parser PLY: precedencia, p_error
│   ├── analizador_semantico.py     # AnalizadorSemantico: compone los mixins de checker/
│   ├── errores.py                  # Lista global de errores: reportar() y limpiar()
│   ├── recorrer_ast.py             # RecorrerAST: despacho visitar_<Clase>
│   ├── ast.py                      # Nodo (línea, columna) y Programa
│   ├── sintax/                     # Reglas de la gramática, un archivo por construcción
│   ├── ast_modular/                # Clases de nodos del AST
│   ├── checker/                    # Validación semántica y tabla de símbolos
│   │   ├── tabla_simbolos.py       # TablaSimbolos, SimboloVariable, SimboloFuncion, SimboloStruct
│   │   └── helpers.py              # Mensajes de error y reglas de tipos compartidas
│   ├── interpreter/                # Intérprete (modo alterno de ejecución)
│   ├── visitor/grafo.py            # AST → DOT → PNG con Graphviz
│   ├── reportes/
│   │   ├── errores.py              # Tabla de errores (fragmento, orden, formato)
│   │   ├── simbolos.py             # Filas de la tabla de símbolos con la columna «Valor»
│   │   ├── simbolos_html.py        # Reporte HTML de símbolos en build/reportes/
│   │   ├── interprete_valores.py   # InterpreteConValores: último valor por sym_id
│   │   └── formato_valor.py        # Formato de valores y valores por defecto
│   └── arm64/                      # Generación de ARM64
│       ├── generador.py            # GeneradorARM64: recorre el AST validado y arma programa.s
│       ├── emisor.py               # Buffer de líneas, etiquetas y comentarios //
│       ├── literales.py            # Literales de texto en .rodata (texto_*, *_len)
│       ├── layout.py               # MarcoFuncion: slots de 16 bytes, prólogo y epílogo
│       ├── programa.py             # ProgramaARM64: _start, funciones y datos
│       ├── errores.py              # ErrorGeneracion y códigos ERR_* de var_globs.s
│       ├── runtime.py              # Ensambla lib/ y la empaqueta en liboxigen.a
│       ├── generacion/             # visitar_* del generador, un módulo por bloque
│       │   ├── tipos.py            # Tipos del checker → celdas, manejadores y descriptores
│       │   ├── constantes.py       # Literales
│       │   ├── variables.py        # let, asignación y asignación compuesta
│       │   ├── aritmetica.py       # Operadores aritméticos, relacionales y lógicos
│       │   ├── control.py          # if, while, loop, for, break y continue
│       │   ├── funciones.py        # Funciones, llamadas y return (x0-x7 y pila)
│       │   ├── impresion.py        # println! con tabla de manejadores
│       │   ├── match.py            # match
│       │   ├── arreglos.py         # Arreglos planos en row-major
│       │   └── strings.py          # String y funciones embebidas
│       ├── pipeline/               # De programa.s a la salida de QEMU, un módulo por etapa
│       │   ├── compilar.py         # compilar_y_ejecutar y construir_y_ejecutar
│       │   ├── resultado.py        # ResultadoARM64 y cronómetro por etapa
│       │   ├── carpetas.py         # build/arm64/<uuid>/ y poda de carpetas antiguas
│       │   ├── herramientas.py     # as, ld, qemu y herramientas faltantes
│       │   ├── biblioteca.py       # liboxigen.a cacheada
│       │   ├── ensamblado.py       # as y traducción de sus errores
│       │   ├── enlace.py           # ld y traducción de sus errores
│       │   └── ejecucion.py        # qemu-aarch64, tiempo límite, señales y errores de ox_error
│       └── lib/                    # Biblioteca de ejecución (sustituye a libc): una rutina por archivo
│           ├── var_globs.s         # Constantes .equ y códigos de error
│           ├── sistema/            # ox_print, ox_print_err, ox_terminar
│           ├── conversion/         # ox_int_to_str
│           ├── impresion/          # ox_print_nl, ox_print_i32, ox_print_f64, ox_print_bool,
│           │                       # ox_print_char(_debug), ox_print_string(_debug), ox_print_array
│           ├── memoria/            # ox_reservar, ox_copiar
│           ├── strings/            # ox_concatenar, ox_repetir, ox_comparar_texto, ox_buscar_texto
│           ├── embebidas/          # ox_len, ox_contains, ox_replace, ox_split, ox_to_uppercase,
│           │                       # ox_to_lowercase, ox_reverse, ox_reverse_array, ox_random
│           └── errores/            # ox_error
│
├── frontend/                       # Capa de presentación (Astro, puerto 4321)
│   ├── public/logoOX.svg
│   └── src/
│       ├── pages/dashboard.astro   # El IDE: compone los componentes
│       ├── layouts/Layout.astro    # Estilos base y tema claro/oscuro
│       ├── components/             # BarraHerramientas, PanelEditor, PanelArm64, Consola, PanelReportes
│       ├── scripts/                # main.ts (conexión), api.ts, editor.ts, archivo.ts, consola.ts,
│       │   │                       # arm64.ts, tema.ts, html.ts
│       │   └── reportes/           # errores.ts, simbolos.ts, ast.ts, tokens.ts, pestanas.ts, menu.ts
│       └── styles/ide.css          # Distribución de los paneles
│
├── docs/                           # Documentación técnica, diagramas y manual de usuario
├── assets/ast/                     # PNG del AST de cada compilación (ignorado por git)
├── build/                          # arm64/<uuid>/ (programa.s, .o, binario), liboxigen.a,
│                                   # reportes/ (HTML de símbolos). Ignorado por git
├── start.sh                        # Levanta backend y frontend
├── pyproject.toml · uv.lock        # Dependencias de Python (uv)
└── test.ox                         # Programa de prueba manual
```

`backend/parsetab.py` y `backend/parser.out` los genera PLY al importar el parser y no se
versionan.
