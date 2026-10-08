"""Texto de la columna «Valor» del reporte de símbolos, a partir del valor Python del intérprete
y del tipo que dejó el checker ('i32', 'String', '[[i32; 3]; 2]', '&[i32]', nombre de struct)."""
from backend.checker.tabla_simbolos import SIN_VALOR
from backend.interpreter.runtime import InstanciaStruct

_POR_DEFECTO = {'i32': '0', 'f64': '0.0', 'bool': 'false', 'char': "'\\0'", 'String': '""'}

def formatear(valor, tipo):
    if valor is None:
        return por_defecto(tipo)
    if isinstance(valor, bool):
        return 'true' if valor else 'false'
    if isinstance(valor, str):
        if tipo == 'char':
            return "'\\0'" if valor == '\0' else f"'{valor}'"
        return f'"{valor}"'
    if isinstance(valor, list):
        interior = _elemento(tipo)
        return '[' + ', '.join(formatear(v, interior) for v in valor) + ']'
    if isinstance(valor, InstanciaStruct):
        return '{' + ', '.join(f'{campo}: {formatear(v, None)}' for campo, v in valor.campos.items()) + '}'
    return str(valor)

def por_defecto(tipo):
    """Valor de una variable que nunca recibió valor: el de su tipo, o «—» si no lo tiene."""
    if tipo in _POR_DEFECTO:
        return _POR_DEFECTO[tipo]
    if _es_arreglo(tipo):
        cantidad = _longitud(tipo)
        return '[' + ', '.join([por_defecto(_elemento(tipo))] * (cantidad or 0)) + ']'
    return SIN_VALOR

def _es_arreglo(tipo):
    return isinstance(tipo, str) and (tipo.startswith('[') or tipo.startswith('&['))

def _elemento(tipo):
    if not _es_arreglo(tipo):
        return None
    interior = tipo[tipo.index('[') + 1:-1]
    return interior[:interior.rindex(';')].strip() if ';' in interior else interior.strip()

def _longitud(tipo):
    if not tipo.startswith('[') or ';' not in tipo:
        return None
    texto = tipo[tipo.rindex(';') + 1:-1].strip()
    return int(texto) if texto.isdigit() else None
