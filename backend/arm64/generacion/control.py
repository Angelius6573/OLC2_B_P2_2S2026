from backend.ast_modular.bucles import Rango
from backend.arm64.errores import ErrorGeneracion
from backend.arm64.layout import TAMANIO_CELDA
from backend.arm64.generacion.tipos import es_par, es_arreglo, elemento, celdas, longitud, posicion

def visitar_BloqueBare(self, nodo):
    self.bloque(nodo.bloque)

def visitar_Condicional(self, nodo):
    n = self.nuevo_numero()
    si_no, fin = f'si_no_{n}', f'fin_si_{n}'
    self.visitar(nodo.condicion)
    self.e.instr('cbz', 'x0', si_no if nodo.bloque_falso else fin)
    self.bloque(nodo.bloque_verdadero)
    if nodo.bloque_falso:
        self.e.instr('b', fin)
        self.e.etiqueta(si_no)
        if isinstance(nodo.bloque_falso, list):
            self.bloque(nodo.bloque_falso)
        else:
            # else if: el Condicional anidado es una sentencia más
            self.sentencia(nodo.bloque_falso)
    self.e.etiqueta(fin)

def visitar_BucleWhile(self, nodo):
    n = self.nuevo_numero()
    inicio, fin = f'bucle_while_{n}', f'fin_while_{n}'
    self.e.etiqueta(inicio)
    self.visitar(nodo.condicion)
    self.e.instr('cbz', 'x0', fin)
    _cuerpo(self, nodo, continuar=inicio, salir=fin)
    self.e.instr('b', inicio)
    self.e.etiqueta(fin)

def visitar_BucleLoop(self, nodo):
    n = self.nuevo_numero()
    inicio, fin = f'bucle_loop_{n}', f'fin_loop_{n}'
    self.e.etiqueta(inicio)
    _cuerpo(self, nodo, continuar=inicio, salir=fin)
    self.e.instr('b', inicio)
    self.e.etiqueta(fin)

def visitar_BucleFor(self, nodo):
    n = self.nuevo_numero()
    inicio, paso, fin = f'bucle_for_{n}', f'paso_for_{n}', f'fin_for_{n}'
    variable = nodo.variable
    simbolo = self.simbolo(variable.sym_id)
    offset = self.marco.reservar_variable(variable.sym_id)
    simbolo.offset = offset
    if isinstance(nodo.iterable, Rango):
        _for_rango(self, nodo, offset, inicio, paso, fin)
    else:
        _for_arreglo(self, nodo, simbolo.tipo, offset, inicio, paso, fin)

def _for_rango(self, nodo, offset, inicio, paso, fin):
    # for i in a..b: a y b se evalúan una sola vez; el rango excluye a b
    e = self.e
    nombre = nodo.variable.id
    e.comentario(f'for {nombre} in a..b -> [x29, #{offset}]')
    self.visitar(nodo.iterable.inicio)
    self.guardar_slot(offset, False, comentario=nombre)
    self.visitar(nodo.iterable.fin)
    limite = self.temporal()
    self.guardar_slot(limite, False, comentario='límite del rango')
    e.etiqueta(inicio)
    self.cargar_slot(offset, False, 'x9')
    self.cargar_slot(limite, False, 'x10')
    e.instr('cmp', 'x9', 'x10')
    e.instr('b.ge', fin)
    _cuerpo(self, nodo, continuar=paso, salir=fin)
    e.etiqueta(paso)
    self.cargar_slot(offset, False, 'x9')
    e.instr('add', 'x9', 'x9', '#1')
    self.guardar_slot(offset, False, 'x9')
    e.instr('b', inicio)
    e.etiqueta(fin)

def _for_arreglo(self, nodo, tipo_variable, offset, inicio, paso, fin):
    # for x in arreglo: índice oculto; x recibe cada elemento, o una vista si es subarreglo
    e = self.e
    tipo_arreglo = self.tipo(nodo.iterable)
    if not es_arreglo(tipo_arreglo):
        raise ErrorGeneracion(f"No se puede recorrer un valor de tipo '{tipo_arreglo}'",
                              *posicion(nodo))
    elem = elemento(tipo_arreglo)
    nombre = nodo.variable.id
    e.comentario(f'for {nombre} in {tipo_arreglo} -> [x29, #{offset}]')
    self.visitar(nodo.iterable)
    arreglo = self.temporal()
    self.guardar_slot(arreglo, True, comentario='arreglo recorrido')
    indice = self.temporal()
    e.instr('str', 'xzr', f'[x29, #{indice}]', comentario='índice oculto')
    e.etiqueta(inicio)
    self.cargar_slot(indice, False, 'x9')
    self.cargar_slot(arreglo, True, 'x11', 'x10')
    e.instr('cmp', 'x9', 'x10')
    e.instr('b.ge', fin)
    if es_arreglo(elem):
        e.cargar_inmediato('x12', celdas(elem, nodo) * TAMANIO_CELDA)
        e.instr('madd', 'x0', 'x9', 'x12', 'x11')
        e.cargar_inmediato('x1', longitud(elem))
    else:
        e.instr('add', 'x11', 'x11', 'x9, lsl #4')
        if es_par(elem):
            e.instr('ldp', 'x0', 'x1', '[x11]')
        else:
            e.instr('ldr', 'x0', '[x11]')
    self.guardar_slot(offset, es_par(tipo_variable), comentario=nombre)
    _cuerpo(self, nodo, continuar=paso, salir=fin)
    e.etiqueta(paso)
    self.cargar_slot(indice, False, 'x9')
    e.instr('add', 'x9', 'x9', '#1')
    self.guardar_slot(indice, False, 'x9')
    e.instr('b', inicio)
    e.etiqueta(fin)

def _cuerpo(self, nodo, continuar, salir):
    self._bucles.append((nodo.label, continuar, salir))
    self.bloque(nodo.bloque_ambito)
    self._bucles.pop()

def visitar_Break(self, nodo):
    if not self._bucles:
        raise ErrorGeneracion('break fuera de un bucle', *posicion(nodo))
    if nodo.label is None:
        self.e.instr('b', self._bucles[-1][2])
        return
    for etiqueta, _, salir in reversed(self._bucles):
        if etiqueta == nodo.label:
            self.e.instr('b', salir, comentario=f"break '{nodo.label}")
            return
    raise ErrorGeneracion(f"No existe un bucle con la etiqueta '{nodo.label}", *posicion(nodo))

def visitar_Continue(self, nodo):
    # La gramática no le acepta etiqueta: siempre es el bucle más interno
    if not self._bucles:
        raise ErrorGeneracion('continue fuera de un bucle', *posicion(nodo))
    self.e.instr('b', self._bucles[-1][1])
