# Manejo de errores — OxigenScript

**Volver al índice:** [Documentación técnica](DOCUMENTACION_TECNICA.md)

## 6.1 Categorías

| Categoría | Productor | Ejemplo |
|---|---|---|
| `Lexico` | `t_error` del lexer | Carácter no reconocido |
| `Sintactico` | `p_error` del parser | Token inesperado |
| `Semantico` | `AnalizadorSemantico.error` | Tipo incompatible |
| `Ejecucion` | `Interprete.ejecutar` | División por cero |

## 6.2 Formato de los reportes

`backend/errores.py` define una lista global de tuplas `(linea, columna, "[Categoria] mensaje")`:

```python
errores = []

def reportar(categoria, linea, columna, mensaje):
    errores.append((linea, columna, f"[{categoria}] {mensaje}"))

def limpiar():
    errores.clear()
```

El analizador semántico mantiene su propia lista con el mismo formato `(linea, columna, "[Semantico] mensaje")`.

## 6.3 Mensajes legibles para el usuario

El parser usa `tokens_esperados()` para convertir la tabla de acciones internas de PLY en una lista de lexemas legibles, humanizados mediante el mapa `LEXEMA_TIPO` (p. ej. `NUMERO_ENTERO` → "número entero", `FUNCTION` → "fn"). El mensaje típico es:

```
Se esperaba 'identificador' o 'fn'… pero se encontró 'x'
```

## 6.4 Recuperación a nivel léxico

Ante un carácter inválido, `t_error` reporta un error **léxico** y ejecuta `t.lexer.skip(1)`, saltando exactamente un carácter para que el análisis nunca se bloquee.
