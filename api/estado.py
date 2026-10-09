"""Mensaje de estado de la consola de salida."""
_ETAPAS = {'ensamblado': 'el ensamblado (as)', 'enlace': 'el enlace (ld)'}

def estado_sin_ejecutar(hay_errores):
    if hay_errores:
        return {'ok': False, 'message': 'El programa tiene errores y no se ejecutó. '
                                        'Revisa la pestaña Errores.', 'time_ms': None}
    return {'ok': False, 'message': 'No se pudo analizar el programa.', 'time_ms': None}

def estado_ejecucion(modo_pedido, modo_real, arm64, errores_ejecucion, tiempo):
    if arm64 is not None and arm64['stage'] in _ETAPAS and not arm64['success']:
        return {'ok': False, 'message': f'Compilación ARM64 fallida en {_ETAPAS[arm64["stage"]]}.',
                'time_ms': None}
    if modo_real == 'arm64':
        mensaje = 'Compilación exitosa (ARM64). Ejecutado con QEMU'
    elif modo_pedido == 'arm64':
        mensaje = 'Sin soporte ARM64 para este programa. Ejecutado con el intérprete'
    else:
        mensaje = 'Ejecutado con el intérprete'
    mensaje += f' en {tiempo} ms.' if tiempo is not None else '.'
    if errores_ejecucion:
        mensaje += f' {len(errores_ejecucion)} error(es) de ejecución.'
    return {'ok': not errores_ejecucion, 'message': mensaje, 'time_ms': tiempo}
