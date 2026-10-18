from backend.ast_modular.funciones import DeclaracionFuncion
from backend.arm64.emisor import Emisor
from backend.arm64.errores import ErrorGeneracion
from backend.arm64.layout import MarcoFuncion, TAMANIO_SLOT
from backend.arm64.generacion.tipos import es_par, posicion

REGISTROS_ARGUMENTO = 8     # x0-x7: primeros 8 parámetros

def distribuir_argumentos(tipos):
    """Ubicación de cada argumento: ('registro', [x0] o [x0, x1]) o ('pila', k).

    Un escalar usa un registro y un String o arreglo dos consecutivos. Si uno no cabe en
    x0-x7, ese y todos los siguientes van a la pila (como el NGRN de AAPCS64). El llamador y el
    llamado usan esta misma función, así que coinciden siempre.
    """
    ubicaciones = []
    siguiente = 0
    en_pila = 0
    for tipo in tipos:
        necesarios = 2 if es_par(tipo) else 1
        if siguiente + necesarios <= REGISTROS_ARGUMENTO:
            ubicaciones.append(('registro', [f'x{siguiente + i}' for i in range(necesarios)]))
            siguiente += necesarios
        else:
            siguiente = REGISTROS_ARGUMENTO
            ubicaciones.append(('pila', en_pila))
            en_pila += 1
    return ubicaciones

def visitar_Programa(self, nodo):
    funciones = [d for d in nodo.declaraciones if isinstance(d, DeclaracionFuncion)]
    if not any(f.nombre_funcion.nombre_funcion == 'main' for f in funciones):
        raise ErrorGeneracion('El programa no define la función main.')
    # DeclaracionStruct no emite código: instanciar o leer un struct falla en _visitar_generico
    for funcion in funciones:
        self.visitar(funcion)

def visitar_DeclaracionFuncion(self, nodo):
    nombre = nodo.nombre_funcion.nombre_funcion
    self.funcion = self.tabla.buscar_funcion(nombre)
    self.marco = MarcoFuncion(nombre)
    parametros = [s for s in self.tabla.variables_de(nombre) if s.categoria == 'Parámetro']
    for simbolo in parametros:
        simbolo.offset = self.marco.reservar_variable(simbolo.sym_id)

    cuerpo = Emisor()
    self.e = cuerpo
    self.bloque(nodo.bloque_ambito)
    if self.funcion.retorno:
        # Si el cuerpo termina sin return (o un error de runtime saltó el return), devuelve 0
        cuerpo.instr('mov', 'x0', '#0', comentario='sin return: valor por defecto')
        cuerpo.instr('mov', 'x1', '#0')

    # La copia de parámetros se genera al final porque los de la pila se leen por encima del
    # marco, cuyo tamaño solo se conoce al cerrar la función
    entrada = Emisor()
    self.e = entrada
    ubicaciones = distribuir_argumentos([s.tipo for s in parametros])
    for simbolo, (lugar, dato) in zip(parametros, ubicaciones):
        par = es_par(simbolo.tipo)
        if lugar == 'registro':
            self.guardar_slot(simbolo.offset, par, *dato, comentario=f'parámetro {simbolo.nombre}')
        else:
            origen = self.marco.tamanio + dato * TAMANIO_SLOT
            self.cargar_slot(origen, par, 'x9', 'x10', comentario=f'parámetro {simbolo.nombre} (pila)')
            self.guardar_slot(simbolo.offset, par, 'x9', 'x10')
    entrada.anexar(cuerpo)
    self.programa.agregar_funcion(self.marco, entrada)
    self.e = None
    self.marco = None
    self.funcion = None

def visitar_LlamadaFuncion(self, nodo):
    funcion = self.tabla.buscar_funcion(nodo.nombre_funcion)
    if funcion is None:
        raise ErrorGeneracion(f"La función '{nodo.nombre_funcion}' no existe", *posicion(nodo))
    tipos = [tipo for _, tipo in funcion.parametros]
    # Todos los argumentos se evalúan antes de cargar registros: una llamada anidada los pisaría
    temporales = []
    for argumento, tipo in zip(nodo.parametros, tipos):
        if isinstance(argumento, list):
            self.arreglo_literal(argumento, tipo)
        else:
            self.visitar(argumento)
        temporal = self.temporal()
        self.guardar_slot(temporal, es_par(tipo), comentario='argumento')
        temporales.append(temporal)

    e = self.e
    ubicaciones = distribuir_argumentos(tipos)
    en_pila = sum(1 for lugar, _ in ubicaciones if lugar == 'pila')
    reserva = en_pila * TAMANIO_SLOT
    if reserva:
        e.instr('sub', 'sp', 'sp', f'#{reserva}', comentario='argumentos que no caben en x0-x7')
        for temporal, tipo, (lugar, k) in zip(temporales, tipos, ubicaciones):
            if lugar == 'pila':
                self.cargar_slot(temporal, es_par(tipo), 'x9', 'x10')
                e.instr('str', 'x9', f'[sp, #{k * TAMANIO_SLOT}]')
                if es_par(tipo):
                    e.instr('str', 'x10', f'[sp, #{k * TAMANIO_SLOT + 8}]')
    for temporal, tipo, (lugar, registros) in zip(temporales, tipos, ubicaciones):
        if lugar == 'registro':
            self.cargar_slot(temporal, es_par(tipo), *registros)
    e.instr('bl', nodo.nombre_funcion)
    if reserva:
        e.instr('add', 'sp', 'sp', f'#{reserva}')

def visitar_Return(self, nodo):
    if nodo.valor is not None:
        if isinstance(nodo.valor, list):
            self.arreglo_literal(nodo.valor, self.funcion.retorno)
        else:
            self.visitar(nodo.valor)
    # El valor queda en x0/x1 y el epílogo restaura x29, x30 y sp
    self.e.instr('b', self.marco.etiqueta_fin)
