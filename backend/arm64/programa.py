from backend.arm64.emisor import Emisor
from backend.arm64.literales import TablaLiterales

class ProgramaARM64:
    """Arma programa.s: cabecera, _start, funciones del usuario y datos de solo lectura.

    _start llama a main y termina con código 0. Las rutinas ox_* viven en backend/arm64/lib/,
    una por archivo, y se enlazan desde liboxigen.a
    """
    def __init__(self):
        self.literales = TablaLiterales()
        self.funciones = Emisor()
        self.datos = Emisor()           # tablas de manejadores y descriptores en .rodata

    def agregar_funcion(self, marco, cuerpo):
        self.funciones.blanco()
        self.funciones.directiva_global(f'.global {marco.nombre}')
        self.funciones.etiqueta(marco.nombre)
        marco.emitir_prologo(self.funciones)
        self.funciones.anexar(cuerpo)
        marco.emitir_epilogo(self.funciones)

    def texto(self):
        salida = Emisor()
        salida.comentario('programa.s: generado por OxigenNative. Se enlaza con liboxigen.a (backend/arm64/lib/).')
        salida.directiva_global('.include "var_globs.s"')
        salida.blanco()
        salida.directiva_global('.global _start')
        salida.seccion('.text')
        salida.etiqueta('_start')
        salida.instr('bl', 'main')
        salida.instr('mov', 'x0', '#0')
        salida.instr('bl', 'ox_terminar')
        salida.anexar(self.funciones)
        salida.blanco()
        self.literales.emitir(salida)
        if self.datos.lineas:
            salida.blanco()
            salida.seccion('.rodata')
            salida.directiva('.align 3')
            salida.anexar(self.datos)
        return salida.texto()
