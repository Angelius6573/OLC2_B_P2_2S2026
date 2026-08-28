# Modelo de ejecución del intérprete — OxigenScript

**Volver al índice:** [Documentación técnica](DOCUMENTACION_TECNICA.md)

OxigenScript es un **intérprete**: no genera código de bajo nivel (ensamblador o código de máquina). En su lugar, recorre el **AST** en tiempo de ejecución y ejecuta cada nodo directamente. Esta sección describe ese mecanismo.

## 4.1 Despacho por reflexión

El núcleo del recorrido está en `backend/recorrer_ast.py`. El método `visitar(nodo)` resuelve, por el nombre de la clase concreta, el método `visitar_{NombreClase}`; si no existe, cae a `_visitar_generico`.

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

Tanto el analizador semántico como el intérprete enlazan sus funciones `visitar_*` como atributos de clase (p. ej. `visitar_OperacionBinaria = visitar_OperacionBinaria`), de modo que el despacho se resuelve por convención de nombres.

## 4.2 Modelo de memoria y ámbitos

El intérprete (`backend/interpreter/interprete.py`) mantiene:

- `ambito_global`: ámbito raíz.
- `ambito_actual`: puntero mutable al ámbito vigente.
- `funciones` y `structs`: registros globales.
- `_funciones_embebidas`: diccionario de funciones integradas.

Los ámbitos se modelan como una **cadena de padres**:

```python
class Ambito:
    __slots__ = ('variables', 'padre')
    def declarar(self, nombre, valor, mutable=False): ...   # sobreescribe silencioso
    def asignar(self, nombre, valor): ...                    # respeta mutabilidad
    def buscar(self, nombre): ...                            # recorre hacia arriba
```

`_ejecutar_bloque(bloque)` crea un `Ambito` hijo, ejecuta las sentencias y restaura el ámbito anterior en un bloque `finally` (scoping léxico).

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

## 4.3 Control de flujo no local mediante excepciones

Las transferencias de control (retorno de función, `break`, `continue`) se implementan con excepciones internas:

- `_ReturnValue` — capturada en `_llamar_funcion`.
- `_BreakSignal(label)` — capturada en los bucles; compara la etiqueta.
- `_ContinueSignal` — capturada en los bucles.

Esto simplifica el salto no local dentro de un recorrido recursivo y soporta `break 'etiqueta` (si la etiqueta no coincide, la excepción se relanza hacia el bucle correcto).

## 4.4 Captura de salida

La API captura el `stdout` del intérprete con `io.StringIO` + `contextlib.redirect_stdout`, de modo que la salida del `println!` se devuelve como cadena en la respuesta de `/api/compile`.

## 4.5 Generación del grafo del AST (PNG)

`backend/visitor/grafo.py` usa **Graphviz** (`Digraph('AST', format='png')`, `rankdir='TB'`). El `VisitarGrafo` recorre el AST y crea un nodo por cada clase (etiqueta = nombre de clase + atributos escalares) y aristas a sus hijos. `renderizar()` guarda el resultado en `assets/ast/` con nombre único `ast_<milisegundos>.png` y devuelve el nombre del archivo, que la API sirve en `/api/ast/{filename}`.
