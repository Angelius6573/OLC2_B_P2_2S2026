"""Mensaje de estado de la consola de salida."""
_ETAPAS = {'ensamblado': 'el ensamblado (as)', 'enlace': 'el enlace (ld)'}
_DE_ANALISIS = ('Lexico', 'Sintactico', 'Semantico')

def estado_sin_ejecutar(hay_errores):
    if hay_errores:
        return {'ok': False, 'message': 'El programa tiene errores y no se ejecutó. '
                                        'Revisa la pestaña Errores.', 'time_ms': None}
    return {'ok': False, 'message': 'No se pudo analizar el programa.', 'time_ms': None}

def estado_ejecucion(modo_pedido, modo_real, arm64, tiempo, filas_errores):
    """`filas_errores` es la tabla ya normalizada: los errores repetidos no cuentan."""
    if arm64 is not None and arm64['stage'] in _ETAPAS and not arm64['success']:
        return {'ok': False, 'message': f'Compilación ARM64 fallida en {_ETAPAS[arm64["stage"]]}.',
                'time_ms': None}
    de_analisis = sum(fila['categoria'] in _DE_ANALISIS for fila in filas_errores)
    de_ejecucion = sum(fila['categoria'] == 'Ejecucion' for fila in filas_errores)
    if modo_real == 'arm64':
        mensaje = 'Compilación exitosa (ARM64). Ejecutado con QEMU'
    elif modo_pedido == 'arm64' and de_analisis:
        mensaje = 'Hay errores semánticos: no se generó ARM64. Ejecutado con el intérprete'
    elif modo_pedido == 'arm64':
        mensaje = 'Sin soporte ARM64 para este programa. Ejecutado con el intérprete'
    else:
        mensaje = 'Ejecutado con el intérprete'
    mensaje += f' en {tiempo} ms.' if tiempo is not None else '.'
    if de_analisis:
        mensaje += f' {de_analisis} error(es) de análisis.'
    if de_ejecucion:
        mensaje += f' {de_ejecucion} error(es) de ejecución.'
    if de_analisis or de_ejecucion:
        mensaje += ' Revisa la pestaña Errores.'
    return {'ok': not (de_analisis or de_ejecucion), 'message': mensaje, 'time_ms': tiempo}
