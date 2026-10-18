# Decisiones de diseño y desafíos enfrentados

**Volver al índice:** [Documentación técnica](DOCUMENTACION_TECNICA.md)

## 1. Herramientas

- **PLY (Python Lex-Yacc)**, como pide el enunciado. Genera tablas LALR, permite declarar la
  precedencia y deja definir los tokens de forma programática. La gramática está repartida en
  `backend/sintax/*.py`, y `analizador_sintactico.py` la importa para que PLY registre cada `p_*`.
- **FastAPI + Uvicorn** para la API y **Astro + TypeScript + CodeMirror** para la GUI. El
  enunciado admite Django, React, Angular u otro framework web.
- **GNU binutils para AArch64 (`as`, `ld`, `ar`) y QEMU User Mode**: la cadena que pide el
  enunciado, sin `gcc` y sin libc.

## 2. Análisis

### 2.1 Modularización por construcción

Cada construcción del lenguaje tiene un archivo por capa: `sintax/`, `ast_modular/`, `checker/`,
`interpreter/` y `arm64/generacion/`. Agregar una construcción toca siempre los mismos lugares
(ver la [guía de modificación](modificacion.md)).

### 2.2 Recorridos por reflexión

`visitar_<Clase>` reduce el acoplamiento, pero un nombre mal escrito cae en `_visitar_generico`.
En el checker eso pasó: `visitar_BloqueBare` existía pero no estaba asignado, así que los bloques
`{ }` no se analizaban. Se corrigió. En el generador ARM64, `_visitar_generico` **lanza un
error**, así que el problema no puede repetirse allí sin que se note.

### 2.3 Recuperación de errores

- **Léxico:** un carácter no reconocido se reporta y se salta (`t.lexer.skip(1)`). Un comentario
  `/*` sin cierre es un error léxico, como pide el enunciado. Su regla va después de la del comentario
  cerrado, porque PLY prueba las reglas de función en orden de definición.
- **Sintáctico:** modo pánico con el token `error` de PLY en dos niveles
  (`declaracion_global : error` e `instruccion : error`). Ambas reglas devuelven `None`, y las
  listas lo descartan, así que el AST queda completo salvo la instrucción con error.
- **Semántico:** el checker acumula errores y sigue. Un mismo programa puede reportar errores
  léxicos, sintácticos y semánticos de líneas distintas en una sola ejecución.

### 2.4 Tabla de símbolos con `sym_id`

Cada declaración recibe un `sym_id` de un contador. Dos variables con el mismo nombre en ámbitos
distintos (*shadowing*) son símbolos distintos. El checker anota el `sym_id` en cada uso, así que
el generador no repite la resolución de nombres. La tabla guarda un historial de todos los
símbolos, porque la pila de ámbitos se vacía al terminar cada función, y el reporte de la tabla
de símbolos necesita verlos todos.

### 2.5 Tipado estricto y promoción

| Operación | Regla |
|---|---|
| `+` | `String + String → String`; entre numéricos, `f64` si los tipos difieren |
| `*` | numéricos; `String * i32` repite el texto |
| `- / %` | numéricos |
| Comparaciones | mismo tipo, o ambos numéricos → `bool` |
| `&& \|\| !` | `bool` |

No hay conversión implícita en asignaciones, llamadas ni retornos.

## 3. Generación de ARM64

### 3.1 Traducción directa y sin libc

El generador emite ARM64 directamente desde el AST, sin código de tres direcciones. El
programa se enlaza con una biblioteca propia, `liboxigen.a`, que sustituye a libc y solo usa
llamadas al sistema. Cada rutina `ox_*` está en su propio archivo `.s`
(`backend/arm64/lib/<tema>/`) con sus propios textos. Así cada rutina se lee, se prueba y se
cambia sola, y el enlazador solo incluye las que el programa usa.

### 3.2 Comentarios con `//`

El código generado y la biblioteca comentan **siempre con `//`**, también en bloques de varias
líneas. El ejemplo de comentarios del enunciado pone `#` después de una instrucción (`mov x0, #10  # comentario`), y
eso no ensambla en AArch64. `#` es el prefijo de los inmediatos, y `aarch64-linux-gnu-as` responde
*unexpected characters following instruction*. `//` es el comentario de línea de GNU `as` para
AArch64 y funciona en cualquier posición.

### 3.3 Registros sin `x19`–`x28`

Los valores viven en memoria (marco de pila y heap), así que el código generado no necesita
registros preservados para guardar estado. Usa `x0`–`x15` y cumple la convención de registros sin guardar nada extra
en cada función. Las rutinas de la biblioteca que usan `x19`–`x22` (por ejemplo
`ox_print_array`) los guardan y restauran.

Hay dos desviaciones documentadas de AAPCS64: el código de error va en `x6`, y los `f64` viajan
por `x0`–`x7` y no por `v0`–`v7` (ver [ARM64](arm64.md#21-registros)).

### 3.4 Variables: tabla de cuatro campos en el compilador, valores en la pila

El modelo `{nombre, tipo, contenido, mutable}` se conserva como **tabla de símbolos del
compilador** (en Python). En ejecución, `contenido` se convierte en el desplazamiento del slot de
la variable en el marco de su función: `[x29, #offset]`. Una tabla global de valores no sirve
cuando una función se llama a sí misma, porque cada llamada necesita sus propias copias.

### 3.5 Celda de 16 bytes

Todo valor ocupa 16 bytes: `+0` es el valor o el puntero, y `+8` la longitud (`String` y
arreglos). Un único tamaño hace que el elemento `i` siempre esté en `base + i·16`, y que la pila
quede alineada a 16 sin cálculos.

### 3.6 Arreglos en row-major

El enunciado pide elegir entre row-major y column-major e indicarlo en el manual técnico. **Se eligió
row-major** (por filas):

- Coincide con el intérprete, que pliega los índices de afuera hacia adentro sobre listas anidadas.
- `m[i]` es una fila contigua, así que se obtiene como una vista `{base + i·C·16, C}` sin copiar.
- La dirección de `m[i][j]` es `base + (i·C + j)·16`, con `C` = elementos por fila. Es la fórmula
  del enunciado.

Todo el arreglo es **un solo bloque contiguo** en el heap. Asignarlo o pasarlo como argumento
comparte el bloque (semántica de referencia), igual que en el intérprete.

### 3.7 Formato de `f64`

`ox_print_f64` redondea a seis decimales con `frinta` y quita los ceros sobrantes: `3.14`,
`0.5`, `2.0 → 2`, `0.0 → 0.0`. El `0.0` se conserva porque es el valor por defecto de un `f64`. Se
eligió `frinta` (redondeo) y no `frintm` (truncamiento) porque con truncamiento `2.675` saldría
`2.674999`.

### 3.8 División entera y módulo

`7 / 2` entre `i32` da `3`: `sdiv` trunca hacia cero (`-7 / 2 = -3`), como Rust. El módulo lleva
el signo del divisor (`-7 % 2 = 1`), como el intérprete. En `f64` se calcula
`a - frintm(a / b) · b`.

### 3.9 Errores de ejecución que no detienen el programa

Un índice fuera de rango o una división entre cero se reportan en stderr con línea y columna, y la
ejecución sigue después de la sentencia que falló, como pide el enunciado en «Resiliencia durante la ejecución».
Como los temporales viven en el marco y `sp` no se mueve a mitad de una expresión, saltar desde
cualquier punto es seguro. Solo el heap agotado es crítico y termina el programa.

### 3.10 Resiliencia en modo ARM64 con errores semánticos

Un programa con errores semánticos no se traduce a ARM64: generar código máquina a partir de
expresiones mal tipadas no es seguro. Aun así, el enunciado pide continuar con la ejecución, y sus
ejemplos de inmutabilidad (imprime `20` y luego el error) y de operadores aritméticos (imprime
`None`) muestran salida. Por
eso, en modo ARM64, un programa con errores semánticos —pero sin errores léxicos ni sintácticos—
**se ejecuta con el intérprete**, y el panel ARM64 lo avisa. Si hay errores léxicos o sintácticos,
el árbol puede estar incompleto y no se ejecuta.

Se descartó que el generador saltara las sentencias con error: es la opción más fiel, pero
obligaba a marcar sentencias en el checker y a tocar el generador al final del proyecto.

### 3.11 Structs y slices por el intérprete

Structs y slices son opcionales en el alcance obligatorio del enunciado. El generador no los traduce:
lanza `ErrorGeneracion`, y la API ejecuta ese programa con el intérprete y lo informa en el panel
ARM64. No se genera código incorrecto.

## 4. Reportes

### 4.1 Formato de error en un solo punto

Los errores salen de cuatro lugares: lexer y parser, checker, intérprete y pipeline ARM64.
Todos usan la misma tupla `(linea, columna, '[Categoría] mensaje')`. En lugar de pasar el código
fuente a cada uno, `backend/reportes/errores.py` arma la tabla al final. Allí separa la categoría,
calcula el fragmento con `^`, ordena por posición, quita duplicados y produce el formato del
enunciado.

### 4.2 Columna

La columna se cuenta **desde 1**, en el inicio del fragmento que causa el error. Un `;` o una `}`
que faltan se reportan justo después del último token. Dos ejemplos del enunciado cuentan desde 0
(caso 4, columna 9; caso 5, columna 12); no se copiaron, para que todos los errores sigan una sola
regla.

### 4.3 Columna «Valor» de la tabla de símbolos

El reporte de la tabla de símbolos muestra el **último valor** de cada variable. El código ARM64 no deja ese
dato a la vista de Python, así que se obtiene de una ejecución aparte del intérprete
(`InterpreteConValores`), sin salida y cortada a un millón de pasos. Esa clase observa sin cambiar
el intérprete. Si una variable nunca se asignó, se muestra el valor por defecto de su tipo.

## 5. Divergencias conscientes con el intérprete

El intérprete del Proyecto 1 se conserva **sin cambios de semántica**. Por eso el modo ARM64 no lo
usa como referencia de salida, y en estos casos dan resultados distintos a propósito:

| Construcción | Intérprete | ARM64 |
|---|---|---|
| `println!("a={} b={:?}", 1, 2)` | `a=2 b=1` (rellena `{:?}` antes que `{}`) | `a=1 b=2` |
| `println!("{}", 2.0)` | `2.0` | `2` |
| `7 / 2` entre `i32` | `3.5` | `3` |
| División entre cero | aborta el programa | reporta y sigue |
| `[[0; 3]; 2]` | las filas son la misma lista | filas independientes |
| `typeof('a')` | `String` | `char` |
| `{:?}` de `char` | `"a"` | `'a'` |

## 6. Desafíos enfrentados

- **Límites de los inmediatos.** `stp x29, x30, [sp, #-N]!` solo admite `N ≤ 504`, y `ldp`/`stp`
  con `[x29, #off]`, de −512 a 504. El prólogo elige entre tres formas según el tamaño, y los
  slots lejanos se leen con `ldr`/`str` separados.
- **El marco solo se conoce al final.** El tamaño depende de todas las variables y temporales de
  la función. El cuerpo se genera en un emisor aparte y después se envuelve con el prólogo y el
  epílogo. Por la misma razón, la copia de los parámetros que llegan por la pila se genera al
  final y se inserta al inicio.
- **Más de ocho argumentos.** Un `String` o un arreglo ocupa dos registros. Lo que no cabe en
  `x0`–`x7` va a la pila del llamador y la función lo lee por encima de su marco.
- **Imprimir `f64` sin printf.** La conversión a texto se escribió a mano con `frinta`, `fcvtzs`
  y `ox_int_to_str`, cuidando los ceros a la izquierda de los decimales (`0.05`) y el acarreo
  (`0.9999999 → 1`).
- **UTF-8.** `char` guarda un punto de código y se codifica al imprimir. `len()` cuenta
  caracteres, y `reverse()` invierte caracteres sin partir sus bytes.
- **Errores de `as` y `ld` legibles.** Se traducen a la línea de `programa.s`, la etiqueta que la
  contiene y la instrucción, para que el error se pueda ubicar.
- **Posición de un `;` faltante.** PLY detecta el error en el token siguiente, que suele estar en
  la línea de abajo. Un envoltorio del lexer recuerda dónde terminó el token anterior, y el error
  se reporta allí, como en el ejemplo de punto y coma faltante del enunciado.
- **Errores repetidos.** En modo intérprete, el intérprete vuelve a fallar en el mismo lugar que
  el checker ya reportó. La tabla omite esos errores de ejecución.
- **Toolchain.** Astro 7 exige Node ≥ 22.12. QEMU escribía volcados de memoria en la carpeta del
  programa ante un `SIGSEGV`, así que se ejecuta con `RLIMIT_CORE = 0`.

## 7. Limitaciones conocidas

1. **Colisión de símbolos.** No hay renombrado automático de los nombres del usuario:
   - Una función que se llama igual que una etiqueta generada (`fin_si_1`) hace fallar a `as` con
     «symbol already defined», y el error se muestra como `[Error de Generación]`.
   - Una función que se llama igual que una rutina del runtime (`ox_print`) **no da error**. `ld`
     ya no extrae esa rutina de `liboxigen.a` y el programa usa la del usuario. El prefijo `ox_`
     queda reservado.
2. **Sin recolección de basura.** El heap de 8 MiB nunca se libera; alcanza para los programas
   del laboratorio.
3. **Structs y slices** se ejecutan con el intérprete en modo ARM64.
4. **Una compilación a la vez:** el estado de errores y el parser de PLY son globales.
