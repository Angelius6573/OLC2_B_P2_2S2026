import re

# Categoría interna -> (columna Tipo de la tabla, encabezado del mensaje)
TIPOS = {
    'Lexico': ('Léxico', 'Error Léxico'),
    'Sintactico': ('Sintáctico', 'Error Sintáctico'),
    'Semantico': ('Semántico', 'Error Semántico'),
    'Ejecucion': ('Ejecución', 'Error de Ejecución'),
    'Generacion': ('Generación', 'Error de Generación'),
}
_CATEGORIA = re.compile(r'^\[(\w+)\]\s*(.*)$', re.DOTALL)

def filas_errores(tuplas, codigo):
    """Tabla de análisis de errores a partir de las tuplas (linea, columna, '[Categoría] mensaje')
    de todos los canales. Ordena por posición, porque PLY intercala errores léxicos y sintácticos, y
    deja al final los que no tienen posición."""
    lineas = codigo.splitlines()
    semanticos = {(linea, columna) for linea, columna, mensaje in tuplas if mensaje.startswith('[Semantico]')}
    filas = []
    for linea, columna, mensaje in sorted(tuplas, key=lambda e: (e[0] <= 0, e[0], e[1])):
        categoria, descripcion = _separar(mensaje)
        if categoria == 'Ejecucion' and semanticos and (linea <= 0 or (linea, columna) in semanticos):
            # El intérprete ejecuta programas con errores semánticos y vuelve a fallar en ellos
            continue
        tipo, encabezado = TIPOS.get(categoria, (categoria, f'Error {categoria}'))
        fragmento = _fragmento(lineas, linea, columna)
        posicion = f' Línea {linea}, Columna {columna}' if linea > 0 else ''
        texto = f'[{encabezado}]{posicion}\n{descripcion}' + (f'\n{fragmento}' if fragmento else '')
        filas.append({
            'no': len(filas) + 1, 'categoria': categoria, 'tipo': tipo, 'linea': linea, 'columna': columna,
            'descripcion': descripcion, 'fragmento': fragmento, 'texto': texto,
        })
    return filas

def _separar(mensaje):
    coincidencia = _CATEGORIA.match(mensaje)
    return (coincidencia.group(1), coincidencia.group(2)) if coincidencia else ('Error', mensaje)

def _fragmento(lineas, linea, columna):
    """La línea del código con un ^ en la columna. Las tabulaciones se copian para que el ^ quede alineado."""
    if not 1 <= linea <= len(lineas):
        return None
    texto = lineas[linea - 1]
    margen = ' ' * len(str(linea))
    if columna < 1:
        return f'{linea} | {texto}'
    antes = texto[:columna - 1]
    sangria = ''.join('\t' if caracter == '\t' else ' ' for caracter in antes) + ' ' * (columna - 1 - len(antes))
    return f'{linea} | {texto}\n{margen} | {sangria}^'
