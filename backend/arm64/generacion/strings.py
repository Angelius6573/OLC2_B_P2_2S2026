"""Strings y funciones embebidas (PLAN §4.2).

Un String es {puntero, longitud en bytes}. Un literal apunta a .rodata y toda operación que
produce texto reserva un bloque nuevo: ningún texto se modifica en sitio, así que compartir el
puntero entre variables es seguro.
"""
from backend.ast_modular.aritmetica import Variable
from backend.ast_modular.arrays import AccederIndice
from backend.arm64.errores import ErrorGeneracion
from backend.arm64.generacion.tipos import es_arreglo, elemento, celdas, posicion

def visitar_DeclaracionString(self, nodo):
    if nodo.metodo == 'new':
        self.e.instr('mov', 'x0', '#0', comentario='String::new()')
        self.e.instr('mov', 'x1', '#0')
    else:
        self.visitar(nodo.valor)

def visitar_FuncionEmbebida(self, nodo):
    generador = _EMBEBIDAS.get(nodo.nombre)
    if generador is None:
        raise ErrorGeneracion(f"La función embebida '{nodo.nombre}' no se puede compilar a ARM64",
                              *posicion(nodo))
    generador(self, nodo)

def _typeof(self, nodo):
    # El tipo es estático: se evalúa el argumento por sus efectos y se carga el nombre del tipo
    argumento = nodo.argumentos[0]
    tipo = self.tipo(argumento)
    self.visitar(argumento)
    self.cargar_texto(tipo)

def _random(self, nodo):
    minimo, maximo = nodo.argumentos
    self.visitar(minimo)
    temporal = self.temporal()
    self.guardar_slot(temporal, False, comentario='mínimo')
    self.visitar(maximo)
    self.e.instr('mov', 'x1', 'x0')
    self.cargar_slot(temporal, False)
    self.e.instr('bl', 'ox_random')

def _len(self, nodo):
    tipo = self.tipo(nodo.objetivo)
    self.visitar(nodo.objetivo)
    if es_arreglo(tipo):
        self.e.instr('mov', 'x0', 'x1', comentario='len() de un arreglo: su longitud exterior')
    else:
        self.e.instr('bl', 'ox_len')

def _con_texto(rutina):
    """Rutina de un argumento: el receptor en x0/x1 y el resultado en x0/x1."""
    def generar(self, nodo):
        self.visitar(nodo.objetivo)
        self.e.instr('bl', rutina)
    return generar

def _contains(self, nodo):
    self.visitar(nodo.objetivo)
    receptor = self.temporal()
    self.guardar_slot(receptor, True, comentario='receptor')
    self.visitar(nodo.argumentos[0])
    self.e.instr('mov', 'x2', 'x0')
    self.e.instr('mov', 'x3', 'x1')
    self.cargar_slot(receptor, True)
    self.e.instr('bl', 'ox_contains')

def _split(self, nodo):
    self.visitar(nodo.objetivo)
    receptor = self.temporal()
    self.guardar_slot(receptor, True, comentario='receptor')
    self.visitar(nodo.argumentos[0])
    self.e.instr('mov', 'x2', 'x0')
    self.e.instr('mov', 'x3', 'x1')
    self.cargar_slot(receptor, True)
    self.e.instr('bl', 'ox_split')

def _replace(self, nodo):
    self.visitar(nodo.objetivo)
    receptor = self.temporal()
    self.guardar_slot(receptor, True, comentario='receptor')
    self.visitar(nodo.argumentos[0])
    buscado = self.temporal()
    self.guardar_slot(buscado, True, comentario='texto buscado')
    self.visitar(nodo.argumentos[1])
    self.e.instr('mov', 'x4', 'x0')
    self.e.instr('mov', 'x5', 'x1')
    self.cargar_slot(buscado, True, 'x2', 'x3')
    self.cargar_slot(receptor, True)
    self.e.instr('bl', 'ox_replace')

def _reverse(self, nodo):
    tipo = self.tipo(nodo.objetivo)
    self.visitar(nodo.objetivo)
    if es_arreglo(tipo):
        # En sitio sobre la dimensión exterior; devuelve el mismo arreglo en x0/x1
        self.e.cargar_inmediato('x2', celdas(elemento(tipo), nodo))
        self.e.instr('bl', 'ox_reverse_array')
        return
    self.e.instr('bl', 'ox_reverse')
    # Igual que el intérprete: el texto invertido se guarda en la variable receptora
    if isinstance(nodo.objetivo, Variable):
        self.guardar_slot(self.marco.offset(nodo.objetivo.sym_id), True,
                          comentario=f'{nodo.objetivo.id} = invertido')

def _push_str(self, nodo):
    """receptor.push_str(texto): concatena y guarda el resultado en el receptor."""
    objetivo = nodo.objetivo
    e = self.e
    if isinstance(objetivo, Variable):
        destino = ('variable', self.marco.offset(objetivo.sym_id))
        self.cargar_slot(destino[1], True, comentario=objetivo.id)
    elif isinstance(objetivo, AccederIndice):
        self.direccion_elemento(objetivo)
        direccion = self.temporal()
        self.guardar_slot(direccion, False, comentario='dirección del receptor')
        destino = ('celda', direccion)
        e.instr('ldp', 'x0', 'x1', '[x0]')
    else:
        raise ErrorGeneracion('push_str necesita una variable o un elemento de arreglo',
                              *posicion(nodo))
    receptor = self.temporal()
    self.guardar_slot(receptor, True, comentario='receptor')
    self.visitar(nodo.argumentos[0])
    e.instr('mov', 'x2', 'x0')
    e.instr('mov', 'x3', 'x1')
    self.cargar_slot(receptor, True)
    e.instr('bl', 'ox_concatenar')
    if destino[0] == 'variable':
        self.guardar_slot(destino[1], True, comentario='push_str')
    else:
        self.cargar_slot(destino[1], False, 'x9')
        e.instr('stp', 'x0', 'x1', '[x9]')

_EMBEBIDAS = {
    'typeof': _typeof,
    'random': _random,
    'len': _len,
    'push_str': _push_str,
    'to_uppercase': _con_texto('ox_to_uppercase'),
    'to_lowercase': _con_texto('ox_to_lowercase'),
    'reverse': _reverse,
    'replace': _replace,
    'contains': _contains,
    'split': _split,
}
