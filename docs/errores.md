# Manejo de errores

**Volver al índice:** [Documentación técnica](DOCUMENTACION_TECNICA.md)

## 1. Formato

Cada error indica su tipo, línea, columna, descripción y el fragmento de código donde se detectó:

```
[Error Sintáctico] Línea 2, Columna 11
Se esperaba ';'.
2 | let x = 10
  |           ^
```

- **Línea y columna** se cuentan desde 1. La columna apunta al inicio del fragmento que causa el
  error: el carácter no reconocido, el valor mal tipado, el nombre de la función llamada o el
  inicio de la expresión que falla. Un `;` o una `}` faltante se reporta justo después del último
  token.
- **Fragmento**: la línea del código con un `^` bajo la columna. Si la línea tiene tabulaciones,
  el `^` las copia para quedar alineado.

## 2. Categorías

| Categoría | Se muestra como | Quién la produce | Ejemplos |
|---|---|---|---|
| `Lexico` | `[Error Léxico]` | `t_error` y la regla de comentario sin cierre del lexer | Carácter no reconocido `'@'`. Comentario de bloque sin cierre |
| `Sintactico` | `[Error Sintáctico]` | `p_error` del parser | Se esperaba `';'`. Se esperaba `'}'`. Token inesperado `';'`. Se esperaba `')'` o `','` |
| `Semantico` | `[Error Semántico]` | `AnalizadorSemantico.error` (`backend/checker/`) | La variable `'x'` no ha sido declarada. Tipos incompatibles. Variable inmutable |
| `Ejecucion` | `[Error de Ejecución]` | `ox_error` en ARM64, el intérprete y QEMU | División por cero. Índice fuera de los límites. Señal o tiempo límite |
| `Generacion` | `[Error de Generación]` | Generador ARM64, `as` y `ld` | Construcción no soportada en ARM64. Error de ensamblado |

Los nueve casos del enunciado y su mensaje:

| # | Caso | Mensaje |
|---|---|---|
| 1 | Carácter no reconocido | `Carácter no reconocido '@'.` |
| 2 | Falta de punto y coma | `Se esperaba ';'.` |
| 3 | Llave o paréntesis sin cerrar | `Se esperaba '}'.` / `Token inesperado ';'. Se esperaba ')' o ','.` |
| 4 | Variable no declarada | `La variable 'total' no ha sido declarada.` |
| 5 | Tipos incompatibles | `No es posible asignar un valor de tipo String a una variable de tipo i32.` / `No es posible aplicar el operador '+' entre los tipos i32 y String.` / `Tipos incompatibles. No es posible utilizar un valor de tipo … donde se esperaba un valor de tipo ….` |
| 6 | Variable inmutable | `No es posible modificar la variable 'contador' porque fue declarada como inmutable.` |
| 7 | Índice fuera de los límites | `Índice fuera de los límites del arreglo 'numeros'.` (con índice constante, en el análisis) o `Índice fuera de los límites del arreglo.` (en ejecución) |
| 8 | Función no declarada | `La función 'saludar' no ha sido declarada.` |
| 9 | Número incorrecto de parámetros | `La función 'suma' esperaba 2 argumentos, pero recibió 1.` |

## 3. Recorrido de un error

Los cuatro productores generan la misma tupla, `(linea, columna, '[Categoría] mensaje')`:

| Canal | Dónde se guarda |
|---|---|
| Léxico y sintáctico | `backend/errores.py`: lista de módulo, `reportar()` y `limpiar()` |
| Semántico | `AnalizadorSemantico.errores` |
| Ejecución en ARM64 | `ResultadoARM64.errores`: las líneas `[Ejecucion] Línea L, Columna C: mensaje` que `ox_error` escribe en stderr, más la señal o el tiempo límite |
| Ejecución en el intérprete | `backend/errores.py`. El intérprete escribe la posición en el texto (`3:10 División por cero`), y `api/modo_interprete.py` la convierte en línea y columna |

Al final, `api/compiler.py` junta todas las tuplas y las pasa por
`backend/reportes/errores.py:filas_errores(tuplas, codigo)`, que:

1. separa la categoría de la descripción;
2. **ordena por posición**, porque PLY intercala errores léxicos y sintácticos, y deja al final
   los que no tienen posición (herramientas faltantes, señales);
3. **quita duplicados**: si hay errores semánticos, un error de ejecución en la misma posición, o
   sin posición, es consecuencia de aquel (el intérprete vuelve a fallar donde el checker ya
   avisó);
4. calcula el fragmento y arma el texto con el formato del enunciado;
5. numera las filas.

Cada fila de la respuesta JSON tiene esta forma:

```json
{
  "no": 1,
  "categoria": "Sintactico",
  "tipo": "Sintáctico",
  "linea": 2,
  "columna": 11,
  "descripcion": "Se esperaba ';'.",
  "fragmento": "2 | let x = 10\n  |           ^",
  "texto": "[Error Sintáctico] Línea 2, Columna 11\nSe esperaba ';'.\n2 | let x = 10\n  |           ^"
}
```

## 4. Recuperación y resiliencia

El compilador sigue después de un error que no es crítico, y reporta varios errores en una sola
ejecución:

- **Léxico:** el carácter inválido se salta (`t.lexer.skip(1)`) y el análisis continúa.
- **Sintáctico:** modo pánico con `instruccion : error` y `declaracion_global : error`. Se descarta
  la instrucción con error y el parser sigue con la siguiente. Si el error está en la cabecera de
  una función o de un struct, se pierde esa declaración completa.
- **Semántico:** el checker acumula los errores y termina de recorrer el programa.
- **Ejecución en ARM64:** `ox_error` reporta y el programa salta al final de la sentencia que
  falló; el resto se ejecuta. Solo el heap agotado termina el programa.
- **Ejecución con errores semánticos:** en modo ARM64 el programa se ejecuta con el intérprete
  (ver [decisiones](decisiones.md#310-resiliencia-en-modo-arm64-con-errores-semánticos)).

Ejemplo de una sola ejecución con errores de las tres fases:

```rust
fn main() {
    let a = @5;
    let b: i32 = "x"
    let c = 3;
    println!(zz);
    c = 4;
}
```

| No | Tipo | Descripción | Línea | Columna |
|---|---|---|---|---|
| 1 | Léxico | Carácter no reconocido '@'. | 2 | 13 |
| 2 | Sintáctico | Se esperaba ';'. | 3 | 21 |
| 3 | Semántico | La variable 'zz' no ha sido declarada. | 5 | 14 |
| 4 | Semántico | No es posible modificar la variable 'c' porque fue declarada como inmutable. | 6 | 5 |

## 5. Mensajes del parser

`p_error` (`backend/analizador_sintactico.py`) decide el mensaje con la tabla de acciones de PLY
para el estado actual:

1. Si se esperaba un cierre (`;`, `}`, `)` o `]`) y el token problemático está en otra línea, o
   el archivo terminó, reporta `Se esperaba '<cierre>'.` al final del token anterior.
2. Si el archivo terminó en otro caso: `Fin de archivo inesperado.`
3. Si no: `Token inesperado '<lexema>'.` Si hay tres opciones válidas o menos, agrega
   `Se esperaba a, b o c.`, con los nombres legibles de `LEXEMA_TIPO` (por ejemplo
   `NUMERO_ENTERO` → «número entero»).

El lexer guarda en cada token su posición final (`token.fin`) y recuerda el token anterior
(`lexer.token_anterior`). Así se reporta la posición correcta aunque PLY detecte el error en el
token siguiente.
