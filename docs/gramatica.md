# Gramática formal

**Volver al índice:** [Documentación técnica](DOCUMENTACION_TECNICA.md)

Gramática de OxigenNative en notación EBNF. Corresponde a las reglas `p_*` de `backend/sintax/` y
de `backend/analizador_sintactico.py`; PLY construye con ellas un analizador LALR. La lista exacta
de producciones que usa PLY está en `backend/parser.out`, que se regenera al cambiar la gramática.
Los terminales (palabras reservadas, operadores, literales y comentarios) están en
[reglas léxicas](lexico.md).

Notación: `{ x }` es cero o más repeticiones, `[ x ]` es opcional, `|` separa alternativas, `ε` es
la cadena vacía y los terminales literales van entre comillas.

## 3.1 Gramática (notación EBNF)

### a) Estructura del programa

```
programa        → { declaracion_global }

declaracion_global → declaracion_funcion
                   | declaracion_struct
                   | error                      (* recuperación panic-mode *)

bloque_ambito   → '{' instrucciones '}'

instrucciones   → { instruccion }

instruccion     → sentencia_imprimir ';'
                 | llamar_funcion ';'
                 | declaracion_variable ';'
                 | corto_circuito ';'
                 | asignar_valor_string ';'
                 | asignacion_variable
                 | asignacion_compuesta
                 | asignacion_indice
                 | condicional
                 | bucle_while
                 | bucle_loop
                 | bucle_for
                 | return_stmt
                 | break_stmt
                 | continue_stmt
                 | match_expr
                 | bloque_bare
                 | error                         (* recuperación panic-mode *)

bloque_bare     → '{' instrucciones '}'          (* scope anónimo como sentencia *)
```

### b) Funciones

```
declaracion_funcion → 'fn' nombre_funcion '(' parametros_funcion ')' valor_retorno bloque_ambito

nombre_funcion      → ID | 'main'

parametros_funcion  → parametros_funcion ',' ID ':' tipo_dato
                     | ID ':' tipo_dato
                     | ε

valor_retorno       → ε | '->' tipo_dato

return_stmt         → 'return' expresion ';' | 'return' ';'

llamar_funcion      → nombre_func_called '(' params_func_called ')'

params_func_called  → params_func_called ',' parametro_call
                     | parametro_call
                     | ε

parametro_call      → valor
```

### c) Variables y asignación

```
declaracion_variable → var_mutable ID tipo_declaracion

var_mutable          → 'let' | 'let' 'mut'

tipo_declaracion     → var_implicita | var_explicita

var_implicita        → '=' valor

var_explicita        → ':' tipo_dato
                      | ':' tipo_dato '=' valor

asignacion_variable  → ID '=' valor ';'

asignacion_compuesta → ID asignador_compuesto operacion_aritmetica ';'

asignador_compuesto  → '+=' | '-=' | '*=' | '/=' | '%='
```

**Valores por defecto** para declaraciones sin inicializador:

| Tipo | Default |
|---|---|
| `i32` | `0` |
| `f64` | `0.0` |
| `bool` | `false` |
| `String` | `""` |
| `char` | `'\0'` |

### d) Tipos de datos

```
tipo_dato          → ID          (* nombre de struct definido por el usuario *)
                    | 'i32' | 'f64' | 'bool' | 'char' | 'String'
                    | tipo_array

tipo_array         → '[' tipo_dato ';' NUMERO_ENTERO ']'   (* [T; N] *)
```

### e) Expresiones y jerarquía de operadores

```
expresion          → operacion_logica | decString | match_expr

valor              → expresion | instanciar_struct

corto_circuito     → operacion_logica
```

**Aritmética:**

```
operacion_aritmetica → operacion_aritmetica ('+' | '-') operadores_multiplicativos
                     | operadores_multiplicativos

operadores_multiplicativos → operadores_multiplicativos ('*' | '/' | '%') operacion_unaria
                           | operacion_unaria

operacion_unaria     → '-' operacion_unaria   %prec NEGACION_UNARIA
                     | operando

operando             → ID | NUMERO_ENTERO | NUMERO_FLOAT | CARACTER
                     | CADENA | RAWSTRING | booleano
                     | nuevo_array | typeof_var | random_var | llamar_funcion
                     | slice_var
                     | '(' operacion_aritmetica ')'
                     | operando '.' ID                                  (* campo *)
                     | operando '[' seleccionar_indice ']'              (* índice *)
                     | operando '.' 'len' '(' ')'
                     | operando '.' 'replace' '(' CADENA ',' CADENA ')'
                     | operando '.' 'to_uppercase' '(' ')'
                     | operando '.' 'to_lowercase' '(' ')'
                     | operando '.' 'contains' '(' CADENA ')'
                     | operando '.' 'split' '(' CADENA ')'
                     | operando '.' 'reverse' '(' ')'

slice_var            → '&' ID '[' seleccionar_indice '..' seleccionar_indice ']'
```

**Relacionales:**

```
operacion_relacional → operacion_relacional ('==' | '!=' | '>=' | '<=' | '>' | '<') operador_relacional
                     | operador_relacional

operador_relacional  → operacion_aritmetica | '(' operacion_relacional ')'
```

**Lógicas:**

```
operacion_logica     → operacion_logica '||' operacion_logica_and
                     | operacion_logica_and

operacion_logica_and → operacion_logica_and '&&' operacion_logica_not
                     | operacion_logica_not

operacion_logica_not → '!' operacion_logica_not | operacion_relacional
```

### f) Control de flujo

```
condicional      → 'if' expresion bloque_ambito
                  | 'if' expresion bloque_ambito 'else' bloque_ambito
                  | 'if' expresion bloque_ambito 'else' condicional   (* else-if *)
```

### g) Bucles (con variantes etiquetadas)

```
bucle_while      → 'while' expresion bloque_ambito
                  | LABEL ':' 'while' expresion bloque_ambito

bucle_loop       → 'loop' bloque_ambito
                  | LABEL ':' 'loop' bloque_ambito

bucle_for        → 'for' ID 'in' rango_for bloque_ambito
                  | LABEL ':' 'for' ID 'in' rango_for bloque_ambito

rango_for        → operacion_aritmetica
                  | operacion_aritmetica '..' operacion_aritmetica

break_stmt       → 'break' ';' | 'break' LABEL ';'
continue_stmt    → 'continue' ';'
```

### h) Match

```
match_expr   → 'match' expresion '{' match_brazos '}'

match_brazos → match_brazos ',' match_brazo
              | match_brazos ','            (* coma final opcional *)
              | match_brazo
              | ε

match_brazo  → match_patron '=>' match_cuerpo

match_cuerpo → expresion | sentencia_imprimir

match_patron → NUMERO_ENTERO | NUMERO_FLOAT | CARACTER | CADENA | RAWSTRING
              | booleano | '_'
```

### i) Structs (definición, instanciación y anidación)

```
declaracion_struct → 'struct' ID bloque_struct

bloque_struct      → '{' contenido_struct '}'

contenido_struct   → lista_campos_struct [ ',' ]

lista_campos_struct → parametros_struct
                     | lista_campos_struct ',' parametros_struct

parametros_struct  → ID ':' td_parametro_struct

instanciar_struct  → ID '{' params_struct [ ',' ] '}'

params_struct      → params_struct ',' param_struct | param_struct | ε

param_struct       → ID ':' valor
```

Como `param_struct → ID ':' valor` y `valor → instanciar_struct`, los **structs anidados** se soportan de forma natural (un campo puede ser otro literal de struct).

### j) Arrays y slices

```
nuevo_array         → '[' arrays ']'
                     | '[' valor ';' operacion_aritmetica ']'      (* repetidor [x;n] *)

arrays              → arrays ',' valor | valor

seleccionar_indice  → operacion_aritmetica

asignacion_indice   → operando '[' seleccionar_indice ']' '=' valor ';'
                     | operando '[' i ']' '[' j ']' '=' valor ';'  (* 2-D *)
```

### k) Strings

```
decString            → 'String' ':' ':' tipo_dec_string

tipo_dec_string      → from_directo | new_posterior

from_directo         → 'from' '(' tipo_cadena ')'      (* String::from(...) *)
new_posterior        → 'new' '(' ')'                   (* String::new() *)

tipo_cadena          → CADENA | RAWSTRING

asignar_valor_string → operando '.' 'push_str' '(' expresion ')'     (* sentencia *)
```

`push_str` acepta cualquier expresión; el análisis semántico exige que sea de tipo `String`.

### l) Impresión

```
sentencia_imprimir  → 'println!' '(' argumentos_impresion ')'

argumentos_impresion → CADENA
                      | CADENA ',' operaciones_directas
                      | RAWSTRING
                      | RAWSTRING ',' operaciones_directas
                      | operaciones_directas            (* println!(a, b, c) *)

operaciones_directas → operaciones_directas ',' valor | valor
```

Los marcadores `{}` (formato normal) y `{:?}` (formato de depuración) se reemplazan de izquierda a
derecha. Sin cadena de formato (`println!(a, b, c)`), los valores se imprimen separados por un
espacio. Una cadena cruda (`r"..."`) no admite argumentos.

### m) Funciones embebidas

```
typeof_var   → 'typeof' '(' operando ')'     (* devuelve tipo: String *)
random_var   → 'random' '(' only_enteros ',' only_enteros ')'   (* devuelve i32 *)
```

| Forma gramatical | Nombre | Comportamiento |
|---|---|---|
| `expr.len()` | `len` | Longitud de string/array |
| `expr.replace(a, b)` | `replace` | Reemplazo de subcadena |
| `expr.to_uppercase()` | `to_uppercase` | Texto en mayúsculas |
| `expr.to_lowercase()` | `to_lowercase` | Texto en minúsculas |
| `expr.contains(s)` | `contains` | Pertinencia de subcadena |
| `expr.split(s)` | `split` | Divide y devuelve array |
| `expr.reverse()` | `reverse` | Invierte string o array (escribe de vuelta) |
| `expr.push_str(s)` | `push_str` | Concatena y muta la variable (sentencia) |

## 3.2 Precedencia y asociatividad de operadores

Definida en `precedence` (de menor a mayor precedencia):

| Nivel | Operadores | Asociatividad |
|---|---|---|
| 1 | `\|\|` | izquierda |
| 2 | `&&` | izquierda |
| 3 | `==` `!=` `>=` `<=` `>` `<` | izquierda |
| 4 | `+` `-` | izquierda |
| 5 | `*` `/` `%` | izquierda |
| 6 | unario `-`, `!` | **derecha** |

Los paréntesis `( ... )` permiten sobreescribir la precedencia.
