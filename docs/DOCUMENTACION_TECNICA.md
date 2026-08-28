# Documentación Técnica — OxigenScript

**Autor:** Angel Raúl Herrera Chilel
**Carnet:** 202402587
**Sección:** B
**Asignatura:** Organización de Lenguajes y Compiladores I

**OxigenScript** es un lenguaje de programación de propósito educativo inspirado en la sintaxis de Rust. Se distribuye como un **intérprete** escrito en Python sobre la librería PLY (Python Lex-Yacc) y se acompaña de un **entorno de desarrollo integrado (IDE) web** que permite escribir, ejecutar y analizar programas.

Este es el índice de la documentación técnica. La documentación está organizada por temas, cada uno en su propio archivo:

| # | Tema | Archivo |
|---|---|---|
| 1 | Arquitectura (pipeline de fases, modularización por feature) | [arquitectura.md](arquitectura.md) |
| 2 | Reglas léxicas (tokens, keywords, operadores) | [lexico.md](lexico.md) |
| 3 | Gramática formal (EBNF) y precedencia de operadores | [gramatica.md](gramatica.md) |
| 4 | Modelo de ejecución del intérprete | [ejecucion.md](ejecucion.md) |
| 5 | Decisiones de diseño y desafíos enfrentados | [decisiones.md](decisiones.md) |
| 6 | Manejo de errores | [errores.md](errores.md) |
| 7 | Estructura de directorios | [estructura.md](estructura.md) |
| 8 | Referencia de la API REST | [api.md](api.md) |

Para el uso funcional de la herramienta se recomienda consultar el **Manual de Usuario** ([manual](manual/MANUAL_USUARIO.tex)).
