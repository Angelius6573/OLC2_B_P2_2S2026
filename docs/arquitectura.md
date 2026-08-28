# Arquitectura — OxigenScript

**Volver al índice:** [Documentación técnica](DOCUMENTACION_TECNICA.md)

## 1. Introducción

OxigenScript es un lenguaje de programación de propósito educativo inspirado en la sintaxis de Rust. Se distribuye como un **intérprete** escrito en Python sobre la librería PLY (Python Lex-Yacc) y se acompaña de un **entorno de desarrollo integrado (IDE) web** que permite escribir, ejecutar y analizar programas.

## 2. Visión general de la arquitectura

OxigenScript implementa un compilador e intérprete en varias fases. El flujo completo de una compilación es:

```
┌────────────┐    ┌────────────┐    ┌────────────────┐    ┌───────────────┐
│  Lexer     │ →  │  Parser    │ →  │     AST        │ →  │  Analizador   │
│  PLY lex   │    │  PLY yacc  │    │                │    │  Semántico    │
└────────────┘    └────────────┘    └────────────────┘    └───────────────┘
                                        │                        │
                                        ▼                        ▼
                                 ┌────────────────┐     ┌───────────────┐
                                 │  Grafo del AST │     │  Intérprete   │
                                 │  (Graphviz)    │     │  (recorre AST)│
                                 └────────────────┘     └───────────────┘
```

### 2.1 Pipeline de fases

1. **Análisis léxico** (`backend/analizador_lexico.py`): convierte la cadena fuente en una secuencia de *tokens* mediante PLY `lex`.
2. **Análisis sintáctico** (`backend/analizador_sintactico.py`): genera las tablas LALR con PLY `yacc` y construye el **Árbol de Sintaxis Abstracta (AST)** aplicando las reglas semánticas de la gramática.
3. **Análisis semántico** (`backend/analizador_semantico.py` + `backend/checker/`): valida tipos, scopes, llamadas a funciones y declaraciones; anota el AST con tipos inferidos.
4. **Generación del grafo del AST** (`backend/visitor/grafo.py`): produce una imagen PNG del árbol con Graphviz.
5. **Interpretación** (`backend/interpreter/`): recorre el AST y ejecuta cada nodo, capturando la salida del `println!`.

### 2.2 Modularización por feature

Una decisión central del proyecto es la **modularización horizontal**: cada constructo del lenguaje tiene un archivo espejo en cada capa.

| Capa | Directorio | Contenido |
|---|---|---|
| Gramática | `backend/sintax/` | Reglas de producción `p_*` de PLY |
| AST | `backend/ast_modular/` | Clases de nodos (subclases de `Nodo`) |
| Semántica | `backend/checker/` | Funciones de validación (`visitar_*`) |
| Interpretación | `backend/interpreter/` | Funciones de ejecución (`visitar_*`) |

Esto mantiene cada feature horizontalmente autónoma y facilita añadir nuevas construcciones sin tocar el núcleo de despacho.
