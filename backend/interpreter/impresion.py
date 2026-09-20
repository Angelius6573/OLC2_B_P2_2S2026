from backend.ast_modular.impresion import Imprimir, ArgumentosImpresion

def _formato_valor(val):
    if isinstance(val, bool):
        return 'true' if val else 'false'
    if val is None:
        return 'None'
    return str(val)

def _formato_debug(val):
    if isinstance(val, list):
        elementos = ', '.join(_formato_debug(item) for item in val)
        return f'[{elementos}]'
    if isinstance(val, bool):
        return 'true' if val else 'false'
    if val is None:
        return 'None'
    if isinstance(val, str):
        return f'"{val}"'
    return repr(val)

def _formato_directo(val):
    if isinstance(val, list):
        return _formato_debug(val)
    return _formato_valor(val)

def visitar_Imprimir(self, nodo):
    args = nodo.argumentos_impresion
    cadena = args.cadena
    operaciones = args.operaciones_directas
    if cadena == '' and operaciones:
        print(' '.join(_formato_directo(self.visitar(op)) for op in operaciones))
        return None
    if operaciones:
        valores = [self.visitar(op) for op in operaciones]
        resultado = cadena
        for val in valores:
            if '{:?}' in resultado:
                resultado = resultado.replace('{:?}', _formato_debug(val), 1)
            elif '{}' in resultado:
                resultado = resultado.replace('{}', _formato_valor(val), 1)
        print(resultado)
    else:
        print(cadena)
    return None
