# Documentación técnica — OxigenNative

**Autor:** Angel Raúl Herrera Chilel
**Carnet:** 202402587
**Curso:** Organización de Lenguajes y Compiladores 2 (0781), sección B
**Proyecto:** Proyecto 2 — compilador a ARM64, segundo semestre de 2026

OxigenNative es un compilador para un lenguaje educativo inspirado en Rust. Analiza el programa
con PLY (léxico, sintáctico y semántico), lo traduce a ensamblador ARM64, lo ensambla y enlaza
con las herramientas GNU para AArch64, y lo ejecuta con QEMU User Mode. El intérprete del Proyecto 1
se conserva como modo alterno. Todo se usa desde un IDE web.

## Índice

| # | Tema | Archivo |
|---|---|---|
| 1 | Arquitectura cliente/servidor y flujo de una compilación | [arquitectura.md](arquitectura.md) |
| 2 | Diagramas de clases y de flujo (AST, tabla de símbolos, pipeline) | [diagramas.md](diagramas.md) |
| 3 | Reglas léxicas: tokens, comentarios, errores léxicos | [lexico.md](lexico.md) |
| 4 | Gramática formal (EBNF) y precedencia | [gramatica.md](gramatica.md) |
| 5 | **Generación de código ARM64**: registros, memoria, traducción, runtime, ensamblado | [arm64.md](arm64.md) |
| 6 | Modo intérprete | [ejecucion.md](ejecucion.md) |
| 7 | Manejo de errores: formato, recuperación, resiliencia | [errores.md](errores.md) |
| 8 | Decisiones de diseño, desafíos y limitaciones | [decisiones.md](decisiones.md) |
| 9 | Estructura de directorios | [estructura.md](estructura.md) |
| 10 | API REST | [api.md](api.md) |
| 11 | Guía de modificación del código | [modificacion.md](modificacion.md) |

**Manual de usuario:** [manual/MANUAL_USUARIO.md](manual/MANUAL_USUARIO.md): instalación, uso del
IDE, lectura de los reportes, capturas y sesiones de ejemplo. Los programas de ejemplo
están en [manual/ejemplos/](manual/ejemplos/).

El manual del Proyecto 1 (intérprete) se conserva como referencia en
[OLC2_LAB_PROYECTO1_MU.pdf](OLC2_LAB_PROYECTO1_MU.pdf).

## Dónde está cada requisito del enunciado

| Entregable | Dónde |
|---|---|
| Gramática formal de OxigenNative | [gramatica.md](gramatica.md) y [lexico.md](lexico.md) |
| Métodos utilizados para generar código a bajo nivel | [arm64.md](arm64.md) |
| Decisiones de diseño y desafíos enfrentados | [decisiones.md](decisiones.md) |
| Elección row-major o column-major | [decisiones.md](decisiones.md#36-arreglos-en-row-major) y [arm64.md](arm64.md#48-arreglos-en-row-major) |
| Diagrama de clases y de flujo de procesamiento | [diagramas.md](diagramas.md) |
| Manual de usuario con capturas | [manual/MANUAL_USUARIO.md](manual/MANUAL_USUARIO.md) |
