from backend.arm64.layout import TAMANIO_CELDA
from backend.arm64.generacion.tipos import es_par, es_arreglo, celdas, longitud

def visitar_Variable(self, nodo):
    offset = self.marco.offset(nodo.sym_id)
    self.cargar_slot(offset, es_par(nodo.tipo), comentario=nodo.id)

def visitar_DeclaracionVariable(self, nodo):
    simbolo = self.simbolo(nodo.sym_id)
    offset = self.marco.reservar_variable(nodo.sym_id)
    simbolo.offset = offset
    tipo = nodo.tipo
    self.e.comentario(f'let {nodo.nombre}: {tipo} -> [x29, #{offset}]')
    if nodo.valor is None:
        self.valor_por_defecto(tipo, nodo)
    elif isinstance(nodo.valor, list):
        # El tipo declarado manda: cubre también el literal vacío
        self.arreglo_literal(nodo.valor, tipo)
    else:
        self.visitar(nodo.valor)
    self.guardar_slot(offset, es_par(tipo), comentario=nodo.nombre)
    if self._fin_sentencia is not None:
        # Un error de runtime en el valor saltó el guardado: la variable queda en 0 (o vacía), no
        # con el valor de una vuelta anterior del bucle que la contiene
        saltar = f'fin_let_{self.nuevo_numero()}'
        self.e.instr('b', saltar)
        self.e.etiqueta(self._fin_sentencia)
        self._fin_sentencia = None
        self.guardar_slot(offset, es_par(tipo), 'xzr', 'xzr', comentario=f'{nodo.nombre} tras el error')
        self.e.etiqueta(saltar)

def valor_por_defecto(self, tipo, nodo):
    """Valor por omisión del enunciado: 0, 0.0, false, "" y el arreglo en ceros."""
    if es_arreglo(tipo):
        # ox_reservar entrega el bloque en ceros
        self.e.cargar_inmediato('x0', celdas(tipo, nodo) * TAMANIO_CELDA)
        self.e.instr('bl', 'ox_reservar')
        self.e.cargar_inmediato('x1', longitud(tipo))
    elif tipo == 'String':
        self.e.instr('mov', 'x0', '#0')
        self.e.instr('mov', 'x1', '#0')
    else:
        self.e.instr('mov', 'x0', '#0', comentario=f'{tipo} por defecto')

def visitar_Asignacion(self, nodo):
    simbolo = self.simbolo(nodo.sym_id)
    if isinstance(nodo.valor, list):
        self.arreglo_literal(nodo.valor, simbolo.tipo)
    else:
        self.visitar(nodo.valor)
    self.guardar_slot(self.marco.offset(nodo.sym_id), es_par(simbolo.tipo), comentario=f'{nodo.nombre} =')

def visitar_AsignacionCompuesta(self, nodo):
    # x op= v se genera como x = x op v, con las mismas reglas de tipos que la binaria
    simbolo = self.simbolo(nodo.sym_id)
    offset = self.marco.offset(nodo.sym_id)
    par = es_par(simbolo.tipo)
    temporal = self.temporal()
    self.cargar_slot(offset, par, comentario=nodo.nombre)
    self.guardar_slot(temporal, par)
    self.visitar(nodo.valor)
    self.operar_binaria(nodo.operador[:-1], temporal, simbolo.tipo, self.tipo(nodo.valor), simbolo.tipo, nodo)
    self.guardar_slot(offset, par, comentario=f'{nodo.nombre} {nodo.operador}')
