"""Reporte HTML de la tabla de símbolos: un archivo autónomo por compilación en
build/reportes/, servido por la API en /api/reportes/<archivo>."""
import time
from html import escape
from pathlib import Path

REPORTES = Path(__file__).resolve().parents[2] / 'build' / 'reportes'

COLUMNAS = [('no', 'No.'), ('identificador', 'Identificador'), ('categoria', 'Categoría'),
            ('tipo', 'Tipo'), ('ambito', 'Ámbito'), ('linea', 'Línea'), ('valor', 'Valor')]

_PLANTILLA = '''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Tabla de símbolos - OxigenNative</title>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 32px; color: #1a1028; background: #f8f7fc; }}
  h1 {{ font-size: 20px; color: #5b21b6; }}
  p {{ color: #6b5c82; font-size: 13px; }}
  table {{ border-collapse: collapse; width: 100%; background: #fff; font-size: 14px; }}
  th, td {{ padding: 8px 12px; border-bottom: 1px solid #e0d8f0; text-align: left; }}
  th {{ background: #f0eaf8; color: #5b21b6; }}
  td.valor {{ font-family: monospace; }}
</style>
</head>
<body>
<h1>Reporte de tabla de símbolos</h1>
<p>Generado el {fecha}. {cantidad} símbolo(s).</p>
<table>
<thead><tr>{encabezados}</tr></thead>
<tbody>
{filas}
</tbody>
</table>
</body>
</html>
'''

def escribir_reporte(filas):
    """Escribe el HTML y devuelve el nombre del archivo."""
    REPORTES.mkdir(parents=True, exist_ok=True)
    nombre = f'simbolos_{int(time.time() * 1000)}.html'
    encabezados = ''.join(f'<th>{titulo}</th>' for _, titulo in COLUMNAS)
    cuerpo = '\n'.join(
        '<tr>' + ''.join(_celda(clave, fila[clave]) for clave, _ in COLUMNAS) + '</tr>' for fila in filas)
    (REPORTES / nombre).write_text(_PLANTILLA.format(
        fecha=time.strftime('%Y-%m-%d %H:%M:%S'), cantidad=len(filas),
        encabezados=encabezados, filas=cuerpo), encoding='utf-8')
    return nombre

def _celda(clave, valor):
    clase = ' class="valor"' if clave == 'valor' else ''
    return f'<td{clase}>{escape(str(valor))}</td>'
