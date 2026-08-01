from graphviz import Digraph
from backend.recorrer_ast import RecorrerAST
import subprocess

class VisitarGrafo(RecorrerAST):
    def __init__(self):
        self.grafo = Digraph('AST', format='svg')
        self.grafo.attr(rankdir='TB')
        self.grafo.attr('node', shape='box')
        self.contador = 0

    def _crear_nodo(self, etiqueta: str) -> str:
        self.contador += 1
        nodo_id = f'nodo{self.contador}'
        self.grafo.node(nodo_id, etiqueta)
        return nodo_id

    def _enlazador(self, nodo_padre: str, nodo_hijo) -> None:
        id_hijo = self.visitar(nodo_hijo)
        if id_hijo is None:
            raise TypeError(f'visitar() devolvió None para {type(nodo_hijo).__name__}')
        self.grafo.edge(nodo_padre, id_hijo)

    def renderizar(self):
        self.grafo.render('arbol_sintactico', format='svg')

        subprocess.run(
            ["kitty", "+kitten", "icat", "arbol_sintactico.svg"],
            check=False
        )

        # Eliminar este subproceso cuando lo formatee a la GUI
        subprocess.run(
            ["rm", "arbol_sintactico", "arbol_sintactico.svg"],
            check=True
        )
