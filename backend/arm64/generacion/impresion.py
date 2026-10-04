from backend.arm64.errores import ErrorGeneracion
from backend.arm64.generacion.tipos import es_par, es_arreglo, manejador, posicion

def partir_formato(cadena):
    """'a={} b={:?}' -> [('texto', 'a='), ('valor', False), ('texto', ' b='), ('valor', True)]."""
    segmentos = []
    texto = []
    i = 0
    while i < len(cadena):
        if cadena.startswith('{:?}', i):
            marcador, depuracion = '{:?}', True
        elif cadena.startswith('{}', i):
            marcador, depuracion = '{}', False
        else:
            texto.append(cadena[i])
            i += 1
            continue
        if texto:
            segmentos.append(('texto', ''.join(texto)))
            texto = []
        segmentos.append(('valor', depuracion))
        i += len(marcador)
    if texto:
        segmentos.append(('texto', ''.join(texto)))
    return segmentos

def visitar_Imprimir(self, nodo):
    """println! con su tabla de manejadores en .rodata, despachada con blr"""
    argumentos = nodo.argumentos_impresion
    cadena = argumentos.cadena
    operaciones = argumentos.operaciones_directas

    if argumentos.es_rawstring or not operaciones:
        # Literal: se escribe tal cual, también si trae llaves
        segmentos = [('texto', cadena)] if cadena else []
    elif cadena == '':
        # println!(a, b, c): los valores separados por un espacio
        segmentos = []
        for i in range(len(operaciones)):
            if i:
                segmentos.append(('texto', ' '))
            segmentos.append(('valor', False))
    else:
        # Sustitución posicional, de izquierda a derecha
        segmentos = partir_formato(cadena)
    valores = [s for s in segmentos if s[0] == 'valor']
    if len(valores) != len(operaciones):
        raise ErrorGeneracion(f'println!: {len(valores)} marcadores y {len(operaciones)} argumentos',
                              *posicion(argumentos))

    # Los argumentos se evalúan antes de escribir nada, en orden, en temporales del marco
    evaluados = []
    for operacion in operaciones:
        tipo = self.tipo(operacion)
        self.visitar(operacion)
        temporal = self.temporal()
        self.guardar_slot(temporal, es_par(tipo), comentario='argumento de println!')
        evaluados.append((temporal, tipo))

    pasos = []      # (manejador, carga de x0/x1/x2)
    siguiente = iter(evaluados)
    for clase, dato in segmentos:
        if clase == 'texto':
            pasos.append(('ox_print', ('texto', dato)))
        else:
            temporal, tipo = next(siguiente)
            # Un arreglo siempre se escribe en formato depuración, como la forma directa del intérprete
            pasos.append((manejador(tipo, dato or es_arreglo(tipo)), ('valor', temporal, tipo)))
    pasos.append(('ox_print_nl', None))

    tabla = f'tabla_manejadores_{self.nuevo_numero()}'
    self.programa.datos.etiqueta(tabla)
    for nombre, _ in pasos:
        self.programa.datos.directiva(f'.quad {nombre}')

    e = self.e
    e.comentario(f'println! despachado por {tabla}')
    for k, (nombre, carga) in enumerate(pasos):
        # Un manejador puede pisar x9-x15: la tabla se recarga antes de cada llamada
        e.instr('ldr', 'x9', f'={tabla}')
        e.instr('ldr', 'x10', f'[x9, #{k * 8}]', comentario=nombre)
        if carga is not None and carga[0] == 'texto':
            self.cargar_texto(carga[1])
        elif carga is not None:
            _, temporal, tipo = carga
            self.cargar_slot(temporal, es_par(tipo))
            if es_arreglo(tipo):
                e.instr('ldr', 'x2', f'={self.descriptor(tipo)}')
        e.instr('blr', 'x10')
