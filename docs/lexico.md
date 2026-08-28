# Reglas léxicas (terminales) — OxigenScript

**Volver al índice:** [Documentación técnica](DOCUMENTACION_TECNICA.md)

El lexer define **77 tokens**, formados por:

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

**Nota sobre `LABEL` vs `CARACTER`:** la regla léxica de `LABEL` intenta primero coincidir `'ident`. Si el identificador está seguido de una comilla de cierre, se reinterpreta como un `CARACTER` (p. ej. `'a'` es un carácter, mientras que `'outer` es una etiqueta de bucle).
