# Decisiones de diseño y desafíos enfrentados — OxigenScript

**Volver al índice:** [Documentación técnica](DOCUMENTACION_TECNICA.md)

## 5.1 Uso de PLY (Python Lex-Yacc)

Se eligió PLY por su idoneidad para un curso de compiladores: genera tablas **LALR**, permite declarar precedencia explícitamente y maneja las tablas de tokens de forma programática (dicts de token → regex encadenados con `chain(...)`). La gramática se fragmenta en módulos `backend/sintax/*.py`, importados por star-import, de modo que cada regla `p_*` se registra con el parser.

## 5.2 Modularización horizontal por feature

Cada constructo tiene un archivo por capa. Esta decisión facilita el desarrollo incremental típico de un laboratorio (una feature por etapa) y mantiene la paridad entre `sintax/`, `ast_modular/`, `checker/` e `interpreter/`.

## 5.3 Despacho por reflexión y su riesgo

La convención `visitar_{Clase}` reduce el acoplamiento, pero tiene una desventaja: un error de tipeo en el nombre del método resulta en un **no-op silencioso** (a través de `_visitar_generico`) en lugar de un error claro. Este riesgo se observó directamente durante el desarrollo de los bloques bare, donde `visitar_BloqueBare` existía pero no estaba enlazado en la clase `Interprete`.

## 5.4 Recuperación de errores panic-mode

El parser emplea el token pseudo `error` de PLY a dos niveles para resincronizar tras un error:

```
declaracion_global : error     (* recuperación a nivel superior *)
instruccion        : error     (* recuperación dentro de un bloque *)
```

Ambas reglas devuelven `None`, y los constructores de listas (`p_programa`, `p_instrucciones`) filtran los `None`, de modo que un programa parcialmente validado aún produce un AST interpretable. El conjunto `_SYNC_TOKENS` se declaró como intención de un mecanismo de sincronización explícito, pero nunca se conectó al flujo PLY (queda como código muerto / de diseño).

## 5.5 Semántica como pasada no fatal que anota el AST

El analizador semántico acumula errores (no los lanza) y continúa la verificación, anotando el tipo inferido en `nodo.tipo`. Esto maximiza la cantidad de diagnósticos que se emiten en una sola pasada y permite que el generador del grafo y fases posteriores lean los tipos anotados.

## 5.6 Shadowing vs redefinición

- Las **variables** admiten *shadowing*: `declarar_variable` sobreescribe silenciosamente la entrada del ámbito (retorna `True` siempre), permitiendo redeclarar en el mismo o en ámbitos anidados.
- Las **funciones y structs** son singletons: una redefinición se rechaza con error ("ya está definido").

## 5.7 Promoción de tipos

La función `binaria(op, izq, der)` modela la promoción:

| Operación | Regla |
|---|---|
| `+` | `String + String → String`; numéricos → `f64` si difieren, si no el tipo común |
| `*` | numéricos; `String * i32` (o inverso) → `String` (repetición) |
| `- / %` | numéricos |
| Comparaciones | ambos del mismo tipo o ambos numéricos → `bool` |
| Lógicos `&& \|\|` | ambos `bool` |

**No hay coerción** en asignaciones, llamadas ni retornos: el tipado es estricto.

## 5.8 Divergencias intencionales entre checker e intérprete

Se documenta una divergencia notable: en el **checker**, la variable de un `for` vive dentro del bloque; en el **intérprete**, el `for` la declara en el ámbito circundante. Esto puede afectar comportamientos de scope en algunos programas.

## 5.9 Desafíos técnicos resueltos

- **Precedencia del `NOT` lógico**: se declaró `NOT` y `NEGACION_UNARIA` como asociativas a la derecha con máxima precedencia para que `!a && b` se lea como `(!a) && b`.
- **Desambiguación `'label` vs `'a'`**: la regla `t_LABEL` intenta primero la etiqueta; si hay comilla de cierre, se convierte en `CARACTER`.
- **Structs anidados**: se resolvió haciendo que `param_struct` acepte `valor` (que admite instanciaciones), y que `tipo_dato` acepte `ID` (nombre de struct) como tipo de campo.
- **División entera**: `20 / 4` produce `4` (int) cuando el cociente es exacto; de lo contrario `4.5` (f64).
- **Etiquetas en bucles y `break 'label`**: se añadió el token `LABEL`, se propagó `label` en los nodos de bucle y se implementó el cruce de etiquetas con `_BreakSignal`.
