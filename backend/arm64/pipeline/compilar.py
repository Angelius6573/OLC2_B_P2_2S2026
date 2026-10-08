"""Pipeline ARM64: AST validado -> programa.s -> as -> ld -> qemu-aarch64.

Cada ejecución trabaja en su propia carpeta build/arm64/<uuid>/. liboxigen.a se construye una
sola vez en build/arm64/ y se reconstruye solo cuando cambia algún archivo de lib/.
"""
from pathlib import Path
from backend.arm64.errores import ErrorGeneracion
from backend.arm64.generador import generar_arm64
from backend.arm64.pipeline.carpetas import FUENTE, nueva_carpeta
from backend.arm64.pipeline.ejecucion import TIEMPO_LIMITE, ejecutar
from backend.arm64.pipeline.enlace import enlazar
from backend.arm64.pipeline.ensamblado import ensamblar
from backend.arm64.pipeline.herramientas import herramientas_faltantes
from backend.arm64.pipeline.resultado import ResultadoARM64, cronometro

def compilar_y_ejecutar(programa, tabla, carpeta=None, tiempo_limite=TIEMPO_LIMITE):
    """Genera, construye y ejecuta un AST que el checker validó sin errores."""
    resultado = ResultadoARM64()
    with cronometro(resultado, 'generacion'):
        try:
            resultado.asm = generar_arm64(programa, tabla)
        except ErrorGeneracion as error:
            resultado.errores.append((error.linea, error.columna, f'[Generacion] {error}'))
            return resultado
    return construir_y_ejecutar(resultado.asm, carpeta, tiempo_limite, resultado)

def construir_y_ejecutar(asm, carpeta=None, tiempo_limite=TIEMPO_LIMITE, resultado=None):
    """as -> ld -> qemu-aarch64 sobre un programa.s ya generado."""
    resultado = resultado or ResultadoARM64(asm=asm)
    resultado.etapa = 'ensamblado'
    resultado.carpeta = Path(carpeta) if carpeta else nueva_carpeta()
    resultado.carpeta.mkdir(parents=True, exist_ok=True)
    (resultado.carpeta / FUENTE).write_text(asm, encoding='utf-8')

    faltantes = herramientas_faltantes()
    if faltantes:
        resultado.errores.append((0, 0, f'[Generacion] Faltan herramientas: {", ".join(faltantes)}. Instala binutils-aarch64-linux-gnu y qemu-user'))
        return resultado

    with cronometro(resultado, 'construccion'):
        if not ensamblar(resultado) or not enlazar(resultado):
            return resultado

    with cronometro(resultado, 'ejecucion'):
        ejecutar(resultado, tiempo_limite)
    return resultado
