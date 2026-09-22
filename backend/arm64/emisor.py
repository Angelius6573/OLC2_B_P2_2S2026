SANGRIA = '  '

class Emisor:
    """
    Todo comentario usa `//`: en línea completa, después de una instrucción y en bloques de
    varias líneas (una `//` por línea).
    """
    def __init__(self):
        self.lineas = []

    def seccion(self, nombre):
        self.lineas.append(f'.section {nombre}')

    def directiva(self, texto):
        self.lineas.append(f'{SANGRIA}{texto}')

    def directiva_global(self, texto):
        self.lineas.append(texto)

    def etiqueta(self, nombre):
        self.lineas.append(f'{nombre}:')

    def instr(self, operacion, *operandos, comentario=None):
        # Los saltos van un nivel más adentro que el cmp o subs que los decide
        sangria = SANGRIA * 2 if operacion == 'b' or operacion.startswith('b.') else SANGRIA
        linea = f'{sangria}{operacion}'
        if operandos:
            linea += ' ' + ', '.join(str(o) for o in operandos)
        if comentario:
            # `//` comenta hasta el fin de línea: un salto en el texto rompería la instrucción
            linea += f'  // {str(comentario).replace(chr(10), " ")}'
        self.lineas.append(linea)

    def comentario(self, texto):
        for parte in str(texto).splitlines() or ['']:
            self.lineas.append(f'// {parte}'.rstrip())

    def blanco(self):
        self.lineas.append('')

    def cargar_inmediato(self, registro, valor, comentario=None):
        # mov acepta 16 bits con signo en una instrucción; lo demás va al literal pool
        if -65536 < valor < 65536:
            self.instr('mov', registro, f'#{valor}', comentario=comentario)
        else:
            self.instr('ldr', registro, f'={valor}', comentario=comentario)

    def anexar(self, otro):
        self.lineas.extend(otro.lineas)

    def texto(self):
        return '\n'.join(self.lineas) + '\n'
