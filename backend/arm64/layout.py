from backend.arm64.errores import ErrorGeneracion

TAMANIO_SLOT = 16
TAMANIO_CELDA = 16
TAMANIO_GUARDADO = 16           # x29 y x30 al fondo del marco

LIMITE_STP_PREINDICE = 504      # stp x29, x30, [sp, #-N]! admite N <= 504
LIMITE_SUB_INMEDIATO = 4095     # sub sp, sp, #N sin desplazamiento
LIMITE_OFFSET_LDR = 32760       # ldr xN, [x29, #off]: 4095 * 8
LIMITE_OFFSET_LDP = 504         # ldp/stp xN, xM, [x29, #off]: de -512 a 504

def redondear_16(n):
    return (n + 15) & ~15

class MarcoFuncion:
    """Marco de pila de una función: un slot de 16 bytes por variable y por temporal.

    Disposición, con x29 = sp tras el prólogo:
        [x29, #0]   x29 y x30 guardados
        [x29, #16]  primer slot
        ...
    Los slots no se reutilizan, así que el sombreado y la recursión no se pisan.
    El tamaño solo se conoce al cerrar la función: el generador emite el cuerpo en un
    emisor aparte y después lo envuelve con emitir_prologo y emitir_epilogo.
    """
    def __init__(self, nombre):
        self.nombre = nombre
        self.offsets = {}
        self.temporales = []
        self._siguiente = TAMANIO_GUARDADO

    @property
    def etiqueta_fin(self):
        return f'fin_funcion_{self.nombre}'

    @property
    def tamanio(self):
        return redondear_16(self._siguiente)

    def _reservar(self):
        offset = self._siguiente
        if offset > LIMITE_OFFSET_LDR:
            raise ErrorGeneracion(
                f"El marco de '{self.nombre}' supera {LIMITE_OFFSET_LDR} bytes; "
                'sus variables ya no se alcanzan con ldr [x29, #offset]')
        self._siguiente += TAMANIO_SLOT
        return offset

    def reservar_variable(self, sym_id):
        if sym_id not in self.offsets:
            self.offsets[sym_id] = self._reservar()
        return self.offsets[sym_id]

    def reservar_temporal(self):
        offset = self._reservar()
        self.temporales.append(offset)
        return offset

    def offset(self, sym_id):
        if sym_id not in self.offsets:
            raise ErrorGeneracion(f"La variable {sym_id} no tiene slot en el marco de '{self.nombre}'")
        return self.offsets[sym_id]

    def emitir_prologo(self, emisor):
        n = self.tamanio
        emisor.comentario(f'Marco de {n} bytes: {len(self.offsets)} variables, '
                          f'{len(self.temporales)} temporales')
        if n <= LIMITE_STP_PREINDICE:
            emisor.instr('stp', 'x29', 'x30', f'[sp, #-{n}]!')
        else:
            if n <= LIMITE_SUB_INMEDIATO:
                emisor.instr('sub', 'sp', 'sp', f'#{n}')
            else:
                emisor.instr('ldr', 'x9', f'={n}')
                emisor.instr('sub', 'sp', 'sp', 'x9')
            emisor.instr('stp', 'x29', 'x30', '[sp]')
        emisor.instr('mov', 'x29', 'sp')

    def emitir_epilogo(self, emisor):
        n = self.tamanio
        emisor.etiqueta(self.etiqueta_fin)
        if n <= LIMITE_STP_PREINDICE:
            emisor.instr('ldp', 'x29', 'x30', f'[sp], #{n}')
        else:
            emisor.instr('ldp', 'x29', 'x30', '[sp]')
            if n <= LIMITE_SUB_INMEDIATO:
                emisor.instr('add', 'sp', 'sp', f'#{n}')
            else:
                emisor.instr('ldr', 'x9', f'={n}')
                emisor.instr('add', 'sp', 'sp', 'x9')
        emisor.instr('ret')
