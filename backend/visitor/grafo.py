from graphviz import Digraph
from backend.recorrer_ast import RecorrerAST
from backend.ast import Nodo
import os
import time
import sys

sys.setrecursionlimit(10000)

_ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'assets', 'ast')

class VisitarGrafo(RecorrerAST):
    def __init__(self):
        self.grafo = Digraph('AST', format='png')
        self.grafo.attr(rankdir='TB')
        self.grafo.attr('node', shape='box')
        self.contador = 0

    def _visitar_generico(self, nodo):
        if not isinstance(nodo, Nodo):
            return self._crear_nodo(str(nodo))
        escalares = [
            f'{k}={v}'
            for k, v in vars(nodo).items()
            if v is not None and not isinstance(v, Nodo) and not isinstance(v, list)
        ]
        etiqueta = type(nodo).__name__
        if escalares:
            etiqueta = f'{etiqueta}({", ".join(escalares)})'
        id_nodo = self._crear_nodo(etiqueta)
        for v in vars(nodo).values():
            if isinstance(v, Nodo):
                self._enlazador(id_nodo, v)
            elif isinstance(v, list):
                for item in v:
                    if item is not None:
                        self._enlazador(id_nodo, item)
        return id_nodo

    def _crear_nodo(self, etiqueta: str) -> str:
        self.contador += 1
        nodo_id = f'nodo{self.contador}'
        self.grafo.node(nodo_id, etiqueta)
        return nodo_id

    def _enlazador(self, nodo_padre: str, nodo_hijo) -> None:
        if isinstance(nodo_hijo, list):
            id_hijo = self._crear_nodo(str(nodo_hijo))
            self.grafo.edge(nodo_padre, id_hijo)
            return
        id_hijo = self.visitar(nodo_hijo)
        if id_hijo is None:
            raise TypeError(f'visitar() devolvió None para {type(nodo_hijo).__name__}')
        self.grafo.edge(nodo_padre, id_hijo)

    def renderizar(self, nombre=None):
        os.makedirs(_ASSETS_DIR, exist_ok=True)
        if nombre is None:
            nombre = f'ast_{int(time.time() * 1000)}'
        ruta = os.path.join(_ASSETS_DIR, nombre)
        self.grafo.render(ruta, format='png', cleanup=True)
        return f'{nombre}.png'

    def renderizar_a(self, ruta_completa):
        directorio = os.path.dirname(ruta_completa)
        if directorio:
            os.makedirs(directorio, exist_ok=True)
        self.grafo.render(ruta_completa, format='png', cleanup=True)
        return f'{os.path.basename(ruta_completa)}.png'
