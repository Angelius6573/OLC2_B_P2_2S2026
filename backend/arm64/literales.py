import re
import unicodedata

MAX_PALABRAS = 4
_NOMBRES_SIMBOLO = {
    ' ': 'espacio',
    '\n': 'salto_de_linea',
    '\t': 'tabulador',
    ',': 'coma',
    '.': 'punto',
    ':': 'dos_puntos',
    ';': 'punto_y_coma',
    '=': 'igual',
    '-': 'guion',
    '+': 'mas',
    '*': 'por',
    '/': 'barra',
    '(': 'parentesis',
    ')': 'parentesis',
    '[': 'corchete',
    ']': 'corchete',
}

class TablaLiterales:
    """Literales de texto en .rodata, con etiqueta legible y longitud resuelta en ensamblado.

    "Resultado: " -> texto_resultado y texto_resultado_len
    Un mismo contenido reutiliza su etiqueta, contenidos distintos con el mismo nombre
    reciben _2, _3...
    """
    def __init__(self):
        self._por_contenido = {}
        self._usadas = set()

    def etiqueta(self, contenido):
        if contenido in self._por_contenido:
            return self._por_contenido[contenido]
        base = 'texto_' + _nombre_desde_contenido(contenido)
        nombre = base
        n = 2
        while nombre in self._usadas:
            nombre = f'{base}_{n}'
            n += 1
        self._usadas.add(nombre)
        self._por_contenido[contenido] = nombre
        return nombre

    @staticmethod
    def longitud(etiqueta):
        return f'{etiqueta}_len'

    def emitir(self, emisor):
        if not self._por_contenido:
            return
        emisor.seccion('.rodata')
        for contenido, nombre in self._por_contenido.items():
            emisor.directiva_global(f'{nombre}: .ascii "{escapar_ascii(contenido)}"')
            emisor.directiva(f'.equ {nombre}_len, .-{nombre}')

def _nombre_desde_contenido(contenido):
    sin_tildes = unicodedata.normalize('NFKD', contenido)
    sin_tildes = ''.join(c for c in sin_tildes if not unicodedata.combining(c))
    palabras = re.findall(r'[a-z0-9]+', sin_tildes.lower())
    if palabras:
        return '_'.join(palabras[:MAX_PALABRAS])
    if contenido == '':
        return 'vacio'
    simbolos = []
    for c in contenido:
        nombre = _NOMBRES_SIMBOLO.get(c, 'simbolo')
        if not simbolos or simbolos[-1] != nombre:
            simbolos.append(nombre)
    return '_'.join(simbolos[:MAX_PALABRAS])

def escapar_ascii(contenido):
    # as copia tal cual los bytes UTF-8, por lo que, solo hay que escapar comillas, barras y controles
    partes = []
    for c in contenido:
        if c == '\\':
            partes.append('\\\\')
        elif c == '"':
            partes.append('\\"')
        elif c == '\n':
            partes.append('\\n')
        elif c == '\t':
            partes.append('\\t')
        elif ord(c) < 0x20 or ord(c) == 0x7F:
            partes.append(f'\\{ord(c):03o}')
        else:
            partes.append(c)
    return ''.join(partes)
