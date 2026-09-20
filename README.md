# OxigenNative
Actualizar documentación en algun momento futuro
## Organización de Lenguajes y Compiladores II | Sección B
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/) [![PLY](https://img.shields.io/badge/PLY-Python%20Lex--Yacc-ffd43b?style=flat)](https://www.dabeaz.com/ply/) [![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/) [![Graphviz](https://img.shields.io/badge/Graphviz-DOT-5A7E3E?style=flat&logo=graphviz&logoColor=white)](https://graphviz.org/) [![Astro](https://img.shields.io/badge/Astro-BC52EE?style=flat&logo=astro&logoColor=white)](https://astro.build/) [![FIUSAC](https://img.shields.io/badge/FIUSAC-Facultad%20de%20Ingenieria-blue?style=flat)](https://portal.ingenieria.usac.edu.gt/) [![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-blue?style=flat)](LICENSE)

**OxigenScript** es un lenguaje de programación de propósito educativo inspirado en la sintaxis de Rust. Se distribuye como un **intérprete** escrito en Python sobre la librería PLY (Python Lex-Yacc) y se acompaña de un **entorno de desarrollo integrado (IDE) web** que permite escribir, ejecutar y analizar programas.

- Permite declarar variables con tipado (implícito o explícito), funciones, `structs` anidados, `match`, bucles etiquetados y arreglos.
- Genera reportes automáticos: tabla de **tokens**, **errores** (léxicos, sintácticos y semánticos) y el **grafo del AST** en formato PNG.
- Incluye funciones embebidas como `len`, `replace`, `reverse`, `split`, `typeof` y `random`.

## Documentación
- [Arquitectura](docs/arquitectura.md)
- [Gramática formal](docs/gramatica.md)
- [Reglas léxicas](docs/lexico.md)
- [Modelo de ejecución del intérprete](docs/ejecucion.md)
- [Decisiones de diseño y desafíos](docs/decisiones.md)
- [Manejo de errores](docs/errores.md)
- [Estructura de directorios](docs/estructura.md)
- [Referencia de la API REST](docs/api.md)
- [Documentación técnica (índice)](docs/DOCUMENTACION_TECNICA.md)
- [Manual de usuario (PDF)](docs/MANUAL_USUARIO.tex)

## Tecnología
La **OxigenScript** está enteramente desarrollada en **Python** usando la librería **PLY** (Python Lex-Yacc) para el análisis léxico y sintáctico, **FastAPI + Uvicorn** para el backend de la API REST y **Graphviz** para la generación del grafo del AST. El frontend es un **IDE web** construido con **Astro** y **Preact**, con **CodeMirror** como editor. Todo el proyecto se edita en ArchLinux con NeoVim.

## Instalación en Linux
Descarga del repositorio:
```sh
mkdir -p ~/Desktop/OxigenScript && git clone <url-del-repositorio>
```

### ArchLinux y derivados (Manjaro, EndeavourOS, Garuda Linux, CachyOS)
Descarga e instalación de las dependencias necesarias:
```sh
sudo pacman -S python python-pip graphviz nodejs npm
cd OxigenScript && uv sync && uv run start.sh
```

### Debian/Ubuntu y derivados (Linux Mint, Xubuntu, Pop! OS, Zorin OS, Kali Linux, Elementary OS)
```bash
sudo apt update
sudo apt install python3 python3-pip graphviz nodejs npm
cd OxigenScript && uv sync && uv run start.sh
```

## Instalación en MacOS
```bash
brew install python graphviz node
cd OxigenScript && uv sync && uv run start.sh
```

## Instalación en Windows 11
- Descargar e instalar [Python](https://www.python.org/downloads/) y agregarlo al PATH.
- Descargar e instalar [Graphviz](https://graphviz.org/download/) y agregarlo al PATH.
- Descargar e instalar [Node.js](https://nodejs.org/).
- Instalar las dependencias:
```bash
cd OxigenScript
uv sync
uv run start.sh
```

> **Nota:** también puede iniciar el proyecto sin `uv` usando un entorno virtual clásico:
> `python -m venv .venv && .venv/bin/pip install -e . && ./start.sh`

---
<p align="center">
Copyright © 2026 Angel Raúl Herrera Chilel.
</p>
<p align="center">
El contenido de terceros utilizado en este proyecto se emplea únicamente con fines educativos. Todos los derechos pertenecen a sus respectivos propietarios.
</p>
