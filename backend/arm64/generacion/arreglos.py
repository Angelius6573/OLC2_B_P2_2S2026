"""Arreglos como bloque plano en row-major

El valor de un arreglo es {puntero a su primera celda, cantidad de elementos de la dimensión
exterior}. Indexar un arreglo cuyos elementos son arreglos devuelve una vista
{puntero + i * celdas(T) * 16, N_T}, así que m[i][j] cae en (i * C + j) * 16.
"""
from backend.arm64.errores import ErrorGeneracion
from backend.arm64.layout import TAMANIO_CELDA, LIMITE_OFFSET_LDP, LIMITE_OFFSET_LDR
from backend.arm64.generacion.tipos import es_par, es_arreglo, elemento, celdas, longitud, posicion

def arreglo_literal(self, lista, tipo):
    """[a, b, c]: reserva el bloque completo y escribe cada hoja en su posición lineal."""
    if not es_arreglo(tipo):
        raise ErrorGeneracion('No se puede deducir el tipo del arreglo literal', *_posicion_lista(lista))
    elem = elemento(tipo)
    total = len(lista) * celdas(elem, lista[0] if lista else None)
    self.e.comentario(f'arreglo {tipo}: {total} celdas en el heap')
    self.e.cargar_inmediato('x0', total * TAMANIO_CELDA)
    self.e.instr('bl', 'ox_reservar')
    base = self.temporal()
    self.guardar_slot(base, False, comentario='bloque del arreglo')
    _llenar(self, lista, elem, base, 0)
    self.cargar_slot(base, False)
    self.e.cargar_inmediato('x1', len(lista))

def _llenar(self, lista, elem, base, desplazamiento):
    paso = celdas(elem) * TAMANIO_CELDA
    for i, item in enumerate(lista):
        destino = desplazamiento + i * paso
        if isinstance(item, list):
            _llenar(self, item, elemento(elem), base, destino)
            continue
        self.visitar(item)
        self.cargar_slot(base, False, 'x9')
        self.guardar_en_direccion(elem, 'x9', destino)

def guardar_en_direccion(self, tipo, base, desplazamiento=0):
    """Guarda el valor de x0/x1 en [base + desplazamiento]. Un subarreglo copia sus celdas."""
    e = self.e
    if es_arreglo(tipo):
        e.instr('mov', 'x1', 'x0', comentario='origen: celdas del subarreglo')
        self.sumar_inmediato('x0', base, desplazamiento)
        e.cargar_inmediato('x2', celdas(tipo) * TAMANIO_CELDA)
        e.instr('bl', 'ox_copiar')
        return
    limite = LIMITE_OFFSET_LDP if es_par(tipo) else LIMITE_OFFSET_LDR
    if desplazamiento > limite:
        self.sumar_inmediato(base, base, desplazamiento)
        desplazamiento = 0
    direccion = f'[{base}, #{desplazamiento}]' if desplazamiento else f'[{base}]'
    if es_par(tipo):
        e.instr('stp', 'x0', 'x1', direccion)
    else:
        e.instr('str', 'x0', direccion)

def direccion_elemento(self, nodo):
    """Deja en x0 la dirección del elemento nodo.objetivo[índice], con verificación de rango."""
    if len(nodo.indices) != 1:
        raise ErrorGeneracion('Se esperaba un índice por acceso', *posicion(nodo))
    e = self.e
    tipo_arreglo = self.tipo(nodo.objetivo)
    elem = elemento(tipo_arreglo)
    self.visitar(nodo.objetivo)
    arreglo = self.temporal()
    self.guardar_slot(arreglo, True, comentario='arreglo indexado')
    self.visitar(nodo.indices[0])
    e.instr('mov', 'x11', 'x0', comentario='índice')
    self.cargar_slot(arreglo, True, 'x9', 'x10')
    # Sin signo: un índice negativo también queda fuera de rango
    valido = f'indice_valido_{self.nuevo_numero()}'
    e.instr('cmp', 'x11', 'x10')
    e.instr('b.lo', valido)
    self.error_runtime('ERR_INDICE_FUERA', nodo)
    e.etiqueta(valido)
    paso = celdas(elem, nodo)
    if paso == 1:
        e.instr('add', 'x0', 'x9', 'x11, lsl #4')
    else:
        e.cargar_inmediato('x12', paso * TAMANIO_CELDA)
        e.instr('madd', 'x0', 'x11', 'x12', 'x9', comentario='row-major: i * celdas por fila')

def visitar_AccederIndice(self, nodo):
    elem = nodo.tipo
    self.direccion_elemento(nodo)
    if es_arreglo(elem):
        # Vista sobre la fila: la dirección ya está en x0
        self.e.cargar_inmediato('x1', longitud(elem))
    elif es_par(elem):
        self.e.instr('ldp', 'x0', 'x1', '[x0]')
    else:
        self.e.instr('ldr', 'x0', '[x0]')

def visitar_AsignarIndice(self, nodo):
    acceso = nodo.objetivo
    elem = acceso.tipo
    self.direccion_elemento(acceso)
    direccion = self.temporal()
    self.guardar_slot(direccion, False, comentario='dirección del elemento')
    if isinstance(nodo.valor, list):
        self.arreglo_literal(nodo.valor, elem)
    else:
        self.visitar(nodo.valor)
    self.cargar_slot(direccion, False, 'x9')
    self.guardar_en_direccion(elem, 'x9')

def visitar_Repetidor(self, nodo):
    """[valor; n]: reserva n * celdas(valor) y copia el valor en cada posición."""
    e = self.e
    elem = elemento(nodo.tipo)
    paso = celdas(elem, nodo) * TAMANIO_CELDA
    n = self.nuevo_numero()
    inicio, fin = f'bucle_repetir_{n}', f'fin_repetir_{n}'

    if isinstance(nodo.valor, list):
        self.arreglo_literal(nodo.valor, elem)
    else:
        self.visitar(nodo.valor)
    valor = self.temporal()
    self.guardar_slot(valor, es_par(elem), comentario='valor repetido')
    self.visitar(nodo.cantidad)
    e.instr('cmp', 'x0', '#0')
    e.instr('csel', 'x0', 'x0', 'xzr', 'gt', comentario='una cantidad negativa da el arreglo vacío')
    cantidad = self.temporal()
    self.guardar_slot(cantidad, False, comentario='cantidad')
    e.cargar_inmediato('x9', paso)
    e.instr('mul', 'x0', 'x0', 'x9')
    e.instr('bl', 'ox_reservar')
    base = self.temporal()
    self.guardar_slot(base, False, comentario='bloque del arreglo')
    indice = self.temporal()
    e.instr('str', 'xzr', f'[x29, #{indice}]')

    e.etiqueta(inicio)
    self.cargar_slot(indice, False, 'x9')
    self.cargar_slot(cantidad, False, 'x10')
    e.instr('cmp', 'x9', 'x10')
    e.instr('b.ge', fin)
    self.cargar_slot(base, False, 'x11')
    e.cargar_inmediato('x12', paso)
    e.instr('madd', 'x11', 'x9', 'x12', 'x11')
    if es_arreglo(elem):
        e.instr('mov', 'x0', 'x11')
        self.cargar_slot(valor, False, 'x1')
        e.cargar_inmediato('x2', paso)
        e.instr('bl', 'ox_copiar')
    else:
        self.cargar_slot(valor, es_par(elem))
        self.guardar_en_direccion(elem, 'x11')
    self.cargar_slot(indice, False, 'x9')
    e.instr('add', 'x9', 'x9', '#1')
    self.guardar_slot(indice, False, 'x9')
    e.instr('b', inicio)
    e.etiqueta(fin)
    self.cargar_slot(base, False)
    self.cargar_slot(cantidad, False, 'x1')

def _posicion_lista(lista):
    for item in lista:
        if not isinstance(item, list):
            return posicion(item)
    return 0, 0
