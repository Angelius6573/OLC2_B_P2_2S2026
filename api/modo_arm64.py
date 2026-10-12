from api.modo_interprete import ejecutar_interprete
from backend.arm64.pipeline.compilar import compilar_y_ejecutar

# Tope de la ejecución del intérprete que solo calcula la columna «Valor» en modo ARM64
LIMITE_PASOS_VALORES = 1_000_000

def ejecutar_arm64(programa, tabla):
    """Pipeline ARM64 (as -> ld -> QEMU). Devuelve salida, errores, celdas para «Valor», el bloque `arm64` de la
    respuesta y el modo con el que se ejecutó realmente.

    Si el generador no soporta el programa (structs y slices), se ejecuta con el
    intérprete y el panel ARM64 lo informa con `notice`.
    """
    resultado = compilar_y_ejecutar(programa, tabla)
    bloque = {
        'asm': resultado.asm,
        'stage': resultado.etapa,
        'success': resultado.exito,
        'exit_code': resultado.codigo_salida,
        'stderr': resultado.salida_errores,
        'times': resultado.tiempos,
        'notice': None,
    }
    if resultado.etapa == 'generacion' and resultado.errores:
        _, _, mensaje = resultado.errores[0]
        bloque['notice'] = mensaje.removeprefix('[Generacion] ') + '. Se ejecutó con el intérprete.'
        salida, errores, celdas, tiempo = ejecutar_interprete(programa, tabla)
        bloque['times'] = {**bloque['times'], 'interprete': tiempo}
        return salida, errores, celdas, bloque, 'interprete'

    # De esta ejecución solo se usan los valores: la salida y los errores que cuentan son los de ARM64
    _, _, celdas, _ = ejecutar_interprete(programa, tabla, LIMITE_PASOS_VALORES)
    return resultado.salida, resultado.errores, celdas, bloque, 'arm64'

def ejecutar_con_errores_semanticos(programa, tabla):
    """Resiliencia (enunciado §3.5.1; ejemplos de §3.3.3 y §3.3.5): un programa con errores semánticos
    no se traduce a ARM64, pero se ejecuta con el intérprete, que sigue después de esos errores.
    Devuelve lo mismo que ejecutar_arm64."""
    salida, errores, celdas, tiempo = ejecutar_interprete(programa, tabla)
    bloque = {
        'asm': '',
        'stage': 'generacion',
        'success': False,
        'exit_code': None,
        'stderr': '',
        'times': {'interprete': tiempo},
        'notice': 'El programa tiene errores semánticos: no se generó código ARM64. Se ejecutó con el intérprete.',
    }
    return salida, errores, celdas, bloque, 'interprete'
