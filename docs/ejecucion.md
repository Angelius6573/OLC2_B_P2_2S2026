# Modo intérprete

**Volver al índice:** [Documentación técnica](DOCUMENTACION_TECNICA.md)

El ejecutor principal es el compilador a ARM64 (ver [ARM64](arm64.md)). El **intérprete** del
Proyecto 1 se conserva como modo alterno: se elige en la GUI con «Intérprete» y recorre el AST en
Python en lugar de generar código máquina. La API también lo usa en tres casos del modo ARM64:

- el programa tiene errores semánticos (resiliencia);
- el programa usa structs o slices, que el generador no traduce;
- para calcular la columna «Valor» del reporte de símbolos, con una ejecución aparte y sin salida.

Su semántica se mantuvo **sin cambios** durante el Proyecto 2. Las diferencias con ARM64 están
listadas en [decisiones](decisiones.md#5-divergencias-conscientes-con-el-intérprete).

## 1. Despacho por reflexión

`backend/recorrer_ast.py` resuelve, por el nombre de la clase del nodo, el método
`visitar_<NombreClase>`. Si no existe, usa `_visitar_generico`:

```python
def visitar(self, nodo):
    if isinstance(nodo, list):
        for n in nodo: self.visitar(n)
        return
    if nodo is None:
        return
    metodo = getattr(self, f'visitar_{type(nodo).__name__}', None)
    if metodo is None:
        metodo = getattr(self, '_visitar_generico', None)
    ...
    return metodo(nodo)
```

`Interprete` (`backend/interpreter/interprete.py`) importa sus funciones `visitar_*` desde
`backend/interpreter/` y las asigna como atributos de clase.

## 2. Ámbitos

El intérprete mantiene `ambito_global`, `ambito_actual` (el vigente), `funciones`, `structs` y
el diccionario de funciones embebidas. Un ámbito es una cadena de padres:

```python
class Ambito:
    __slots__ = ('variables', 'padre')
    def declarar(self, nombre, valor, mutable=False): ...
    def asignar(self, nombre, valor): ...     # respeta la mutabilidad
    def buscar(self, nombre): ...             # sube por los padres
```

Cada bloque crea un ámbito hijo y restaura el anterior al salir, aunque haya una excepción:

```python
def _ejecutar_bloque(self, bloque):
    anterior = self.ambito_actual
    self.ambito_actual = Ambito(anterior)
    try:
        for instruccion in bloque:
            self.visitar(instruccion)
    finally:
        self.ambito_actual = anterior
```

## 3. Control de flujo no local

`return`, `break` y `continue` se implementan con excepciones internas:

- `_ReturnValue`, capturada al llamar a una función.
- `_BreakSignal(label)`, capturada por los bucles; si la etiqueta no es la del bucle, se relanza
  hacia el bucle exterior (`break 'externo;`).
- `_ContinueSignal`, capturada por los bucles.

## 4. Errores y salida

Un error de ejecución (`RuntimeError`) detiene el intérprete. `Interprete.ejecutar` lo registra
en `backend/errores.py` con la posición al inicio del texto (`3:10 División por cero`), y
`api/modo_interprete.py` la convierte en línea y columna para la tabla de errores.

La API captura la salida de `println!` con `contextlib.redirect_stdout` sobre un `io.StringIO`.

## 5. Columna «Valor» de la tabla de símbolos

`InterpreteConValores` (`backend/reportes/interprete_valores.py`) es una subclase que observa la
ejecución sin cambiarla. Por cada `sym_id` guarda el objeto de la variable (declaraciones,
variable del `for` y parámetros). Como asignar, `+=` y `push_str` modifican ese mismo objeto, al
final tiene el último valor. Se detiene tras un millón de pasos, para que un bucle infinito no
bloquee el reporte.

## 6. Grafo del AST

`backend/visitor/grafo.py` recorre el AST con `VisitarGrafo`: crea un nodo de Graphviz por cada
nodo del árbol, etiquetado con su clase y sus atributos simples (incluidos `tipo` y `sym_id`
anotados por el checker), y una arista hacia cada hijo. `renderizar()` escribe el archivo DOT y lo
convierte a PNG en `assets/ast/ast_<milisegundos>.png`, que la API sirve en `/api/ast/<archivo>`.
