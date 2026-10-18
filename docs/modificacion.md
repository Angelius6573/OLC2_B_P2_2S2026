# Guía de modificación del código

**Volver al índice:** [Documentación técnica](DOCUMENTACION_TECNICA.md)

El enunciado pide poder modificar una parte del compilador durante la calificación. Esta guía
indica dónde se hace cada tipo de cambio y documenta tres cambios probados de principio a fin.

## 1. Ciclo de trabajo

1. Levantar el proyecto con `uv run start.sh`. El backend corre con `--reload`, así que un cambio
   en un `.py` se aplica al guardar.
2. Hacer el cambio.
3. Comprobarlo desde la GUI (Ejecutar) o sin servidor:

   ```sh
   .venv/bin/python -c "from api.compiler import compilar_codigo; r = compilar_codigo(open('prueba.ox').read()); print(r['output']); [print(e['texto']) for e in r['errors']]"
   ```

   Con `compilar_codigo(codigo, 'interprete')` se prueba el modo intérprete.

Notas:

- **Gramática:** PLY regenera `backend/parsetab.py` y `backend/parser.out` al importar el parser si
  la gramática cambió. Si el parser se comporta raro después de un cambio, borrar esos dos archivos
  obliga a regenerarlos.
- **Biblioteca ARM64:** `liboxigen.a` se reconstruye sola en la siguiente compilación cuando algún
  `.s` de `backend/arm64/lib/` es más reciente que ella.
- **Código generado:** el ensamblador de cada compilación queda en el panel «Código ARM64
  generado» (botón «Descargar .s») y en `build/arm64/<uuid>/programa.s`.

## 2. Dónde tocar

| Quiero cambiar… | Archivo |
|---|---|
| Un mensaje de error léxico | `backend/analizador_lexico.py` (`t_error`, `t_ignore_COMENTARIO_SIN_CIERRE`) |
| Un mensaje de error sintáctico | `backend/analizador_sintactico.py` (`p_error`) |
| Un mensaje de error semántico común | `backend/checker/helpers.py` (`se_esperaba`, `operador_invalido`, `no_declarada`, `inmutable`, `verificar_asignacion`) |
| Una validación semántica | `backend/checker/<construcción>.py` |
| El formato de la tabla de errores | `backend/reportes/errores.py` |
| Una regla de la gramática | `backend/sintax/<construcción>.py` |
| Cómo se traduce una construcción a ARM64 | `backend/arm64/generacion/<bloque>.py` |
| Cómo se imprime un tipo en ARM64 | `backend/arm64/lib/impresion/ox_print_<tipo>.s` y la tabla de `generacion/impresion.py` |
| Un mensaje de error de ejecución en ARM64 | `backend/arm64/lib/errores/ox_error.s` |
| Prólogo, epílogo o tamaño del slot | `backend/arm64/layout.py` |
| El mensaje de estado de la consola | `api/estado.py` |
| La GUI | `frontend/src/components/` y `frontend/src/scripts/` |

## 3. Ensayo 1: cambiar un mensaje de error semántico

**Objetivo:** que el error de variable no declarada sugiera cómo corregirlo.

En `backend/checker/helpers.py`:

```python
def no_declarada(analizador, nodo, nombre):
    analizador.error(nodo.linea, nodo.columna, f"La variable '{nombre}' no ha sido declarada.")
```

cambiar el texto por:

```python
    analizador.error(nodo.linea, nodo.columna,
                     f"La variable '{nombre}' no existe en este ámbito; declárala con let antes de usarla.")
```

**Resultado** con `println!(total);` en la línea 4:

```
[Error Semántico] Línea 4, Columna 14
La variable 'total' no existe en este ámbito; declárala con let antes de usarla.
4 |     println!(total);
  |              ^
```

Como el mensaje vive en un solo helper, el cambio aplica a los tres lugares que lo usan: uso de una
variable, asignación y asignación compuesta.

## 4. Ensayo 2: cambiar una rutina del runtime ARM64

**Objetivo:** que en modo ARM64 los booleanos se impriman en español.

En `backend/arm64/lib/impresion/ox_print_bool.s`, cambiar los dos literales:

```asm
texto_true: .ascii "verdadero"
  .equ texto_true_len, .-texto_true
texto_false: .ascii "falso"
  .equ texto_false_len, .-texto_false
```

La longitud la calcula el ensamblador (`.-texto_true`), así que no hay que tocar nada más.

**Resultado** con `let listo = 3 > 2; println!("{} {}", listo, !listo);` en modo ARM64:

```
verdadero falso
```

`liboxigen.a` se reconstruyó sola. En modo intérprete el mismo programa sigue imprimiendo
`true false`, porque el intérprete no usa la biblioteca ARM64.

## 5. Ensayo 3: agregar una validación semántica

**Objetivo:** reportar en el análisis una división entre la constante `0`, antes de ejecutar.

En `backend/checker/aritmetica.py`, dentro de `visitar_OperacionBinaria`, antes del bloque de los
operadores aritméticos:

```python
    if operador in ('/', '%') and isinstance(nodo.derecha, (NumeroEntero, NumeroFloat)) and nodo.derecha.valor == 0:
        self.error(nodo.linea, nodo.columna, f"El divisor de '{operador}' es la constante 0.")
    if operador in ('+', '-', '*', '/', '%'):
        ...
```

`NumeroEntero` y `NumeroFloat` ya están importados en ese archivo. Se usa la posición de la
operación (`nodo.linea`, `nodo.columna`), que es la regla del proyecto para los errores de una
expresión.

**Resultado** con `let a = 10 / 0;` en la línea 2:

```
[Error Semántico] Línea 2, Columna 13
El divisor de '/' es la constante 0.
2 |     let a = 10 / 0;
  |             ^
```

Ahora es un error semántico, así que en modo ARM64 el programa ya no se traduce y se ejecuta con el
intérprete. La tabla muestra solo el error semántico. El intérprete también falla en esa división,
pero ese error de ejecución está en la misma posición y se omite por duplicado.

## 6. Receta: agregar una construcción al lenguaje

Una construcción nueva toca las mismas capas en este orden:

1. **Token** (si hace falta): en `backend/analizador_lexico.py`, agregarlo al diccionario que
   corresponda (`reserved_words`, `embedded_functions` u operadores). Para que los mensajes de
   error lo nombren bien, agregar su lexema en `LEXEMA_TIPO`.
2. **Nodo:** una clase en `backend/ast_modular/<tema>.py` que herede de `Nodo`.
3. **Regla:** una función `p_*` en `backend/sintax/<tema>.py` que construya el nodo con
   `fijar_ubicacion(t, Nodo(...))`, para que tenga línea y columna. Si el archivo es nuevo, hay que
   importarlo en `backend/analizador_sintactico.py` con `from backend.sintax.<tema> import *`.
4. **Checker:** `visitar_<Nodo>` en `backend/checker/<tema>.py`, que devuelve el tipo y lo anota
   en `nodo.tipo`. Asignarlo en `AnalizadorSemantico` (`visitar_<Nodo> = visitar_<Nodo>`). Si se
   olvida, el nodo no se valida y no aparece ningún error.
5. **Intérprete:** `visitar_<Nodo>` en `backend/interpreter/` y su asignación en `Interprete`.
6. **ARM64:** `visitar_<Nodo>` en `backend/arm64/generacion/<bloque>.py` y su asignación en
   `GeneradorARM64`. Si falta, el generador lanza `ErrorGeneracion` con el nombre del nodo, y la
   API ejecuta el programa con el intérprete.

## 7. Receta: agregar una rutina al runtime

1. Crear `backend/arm64/lib/<tema>/ox_<nombre>.s` con `.global ox_<nombre>` y
   `.include "var_globs.s"`. Va **una rutina por archivo**, con sus textos en su propio `.rodata`.
2. Respetar la convención: argumentos en `x0`–`x7` y resultado en `x0`/`x1`. Se pueden usar
   `x9`–`x15` libremente; si se usan `x19`–`x28`, hay que guardarlos y restaurarlos. Si la rutina
   llama a otra, debe guardar `x29`/`x30` con `stp`.
3. Llamarla desde el generador con `self.e.instr('bl', 'ox_<nombre>')`.

`runtime.py` encuentra el archivo nuevo sola (`lib/**/ox_*.s`), y la biblioteca se reconstruye.

## 8. Receta: agregar un error de ejecución ARM64

1. En `backend/arm64/lib/var_globs.s`, agregar `.equ ERR_NUEVO, 5` y actualizar
   `.equ ERR_ULTIMO, 5`.
2. En `backend/arm64/lib/errores/ox_error.s`, agregar el mensaje en `.rodata` y su entrada
   `.quad mensaje_nuevo, mensaje_nuevo_len` al final de `tabla_errores`, en el orden del código.
3. En el generador, emitir la comprobación y llamar `self.error_runtime('ERR_NUEVO', nodo)`, que
   escribe `mov x6, ERR_NUEVO`, la línea, la columna, `bl ox_error` y el salto al final de la
   sentencia.

Python lee los códigos de `var_globs.s` (`backend/arm64/errores.py`), así que no hay que repetirlos
en otro lado.
