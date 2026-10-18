# Reglas léxicas (terminales)

**Volver al índice:** [Documentación técnica](DOCUMENTACION_TECNICA.md)

El lexer (`backend/analizador_lexico.py`, PLY `lex`) define **77 tokens**, formados por:

- **24 palabras reservadas** (keywords).
- **10 funciones embebidas** (tokens reservados, no utilizables como identificadores).
- **34 operadores y símbolos**.
- **9 tokens** especiales (literales, `println!`, `MATCH_BASE`, `LABEL`, `ID`).

## Palabras reservadas

| Lexema | Token | Lexema | Token |
|---|---|---|---|
| `fn` | `FUNCTION` | `for` | `FOR` |
| `let` | `LET` | `in` | `FOR_IN` |
| `main` | `MAIN` | `loop` | `LOOP` |
| `mut` | `MUT` | `match` | `MATCH` |
| `if` | `IF` | `break` | `BREAK` |
| `else` | `ELSE` | `continue` | `CONTINUE` |
| `while` | `WHILE` | `return` | `RETURN` |
| `struct` | `STRUCT` | `true` / `false` | `TRUE` / `FALSE` |
| `String` | `DT_STRING` | `i32` | `DT_INT` |
| `f64` | `DT_FLOAT` | `bool` | `DT_BOOL` |
| `char` | `DT_CHARACTER` | `from` | `FROMSTRING` |
| `new` | `NEWSTRING` | | |

## Funciones embebidas (reservadas)

| Lexema | Token | Lexema | Token |
|---|---|---|---|
| `typeof` | `TYPEOF` | `to_uppercase` | `MAYUSCULAS` |
| `random` | `RANDOM` | `to_lowercase` | `MINUSCULAS` |
| `len` | `LEN` | `reverse` | `REVERSE` |
| `contains` | `CONTAINS` | `push_str` | `PUSH_STR` |
| `replace` | `REPLACE` | `split` | `SPLIT` |

## Operadores y símbolos

| Categoría | Símbolos |
|---|---|
| Flecha | `=>` |
| Relacionales | `==` `!=` `>=` `<=` `>` `<` |
| Lógicos | `&&` `\|\|` `!` |
| Asignación | `->` `+=` `-=` `*=` `/=` `%=` `=` |
| Aritméticos | `+` `-` `*` `/` `%` |
| Delimitadores | `(` `)` `{` `}` `[` `]` |
| Puntuación | `..` `.` `,` `:` `;` `&` |

## Tokens especiales

| Token | Descripción |
|---|---|
| `ID` | Identificador: `[a-zA-Z_][a-zA-Z_0-9]*` |
| `NUMERO_ENTERO` | Entero: `\d+` (tipo `i32`) |
| `NUMERO_FLOAT` | Flotante: `\d+\.\d+` (tipo `f64`) |
| `CARACTER` | Carácter: `'([^'\\]|\\.)'` |
| `CADENA` | Cadena: `"([^\\"]|\\.)*"` (descodifica `\t`, `\n`, `\"`, `\'`, `\\`) |
| `RAWSTRING` | Cadena cruda: `r"..."` o `r#"..."#` |
| `LABEL` | Etiqueta de bucle: `'ident` |
| `MATCH_BASE` | Comodín `_` en patrones de match |
| `PRINTLN` | Macro `println!` |

## Elementos ignorados

| Elemento | Expresión | Nota |
|---|---|---|
| Espacio y tabulación | `t_ignore = ' \t'` | |
| Salto de línea | `\n+` | Incrementa el número de línea |
| Comentario de línea | `//.*` | |
| Comentario de bloque | `/\*[\s\S]*?\*/` | Puede abarcar varias líneas; se cuentan sus saltos |
| Comentario de bloque sin cierre | `/\*[\s\S]*` | **Error léxico**: `Comentario de bloque sin cierre: falta '*/'.` Consume el resto del archivo |

Los comentarios no generan tokens. La regla del comentario sin cierre se define después de la del
comentario cerrado: PLY prueba las reglas de función en el orden en que se definen, así que solo
se aplica si no hay `*/`.

## Errores léxicos

Un carácter que no inicia ningún token se reporta como `Carácter no reconocido '@'.`, con su línea
y columna, y se salta con `t.lexer.skip(1)`. El análisis continúa (ver [errores](errores.md)).

La columna se calcula a partir de la posición absoluta del token (`contar_columna`), contando
desde 1. Cada token guarda además su posición final (`token.fin`), que el parser usa para ubicar un
`;` o una `}` faltante.

**Nota sobre `LABEL` vs `CARACTER`:** la regla léxica de `LABEL` intenta primero coincidir `'ident`. Si el identificador está seguido de una comilla de cierre, se reinterpreta como un `CARACTER` (p. ej. `'a'` es un carácter, mientras que `'outer` es una etiqueta de bucle).
