from graphviz import Digraph
from backend.recorrer_ast import RecorrerAST
import subprocess

class VisitarNodos(RecorrerAST):
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

        subprocess.run(
            ["rm", "arbol_sintactico", "arbol_sintactico.svg"],
            check=True
        )

    def visitar_Programa(self, nodo):
        id_nodo = self._crear_nodo('Programa')
        for e in nodo.declaraciones:
            self._enlazador(id_nodo, e)
        return id_nodo

    def visitar_DeclaracionFuncion(self, nodo):
        id_nodo = self._crear_nodo('DeclaracionFuncion')
        self._enlazador(id_nodo, nodo.nombre_funcion)
        self.grafo.edge(id_nodo, self._crear_nodo(f'parametros: {nodo.parametros_funcion}'))
        self.grafo.edge(id_nodo, self._crear_nodo(f'valor_retorno: {nodo.valor_retorno}'))
        for inst in nodo.bloque_ambito:
            self._enlazador(id_nodo, inst)
        return id_nodo

    def visitar_DeclaracionStruct(self, nodo):
        id_nodo = self._crear_nodo(f'DeclaracionStruct({nodo.nombre_struct})')
        campos = nodo.parametros_struct
        if isinstance(campos, list):
            for p in campos:
                self._enlazador(id_nodo, p)
        else:
            self._enlazador(id_nodo, campos)
        return id_nodo

    def visitar_Parametros(self, nodo):
        return self._crear_nodo(f'Parametros({nodo.parametro}: {nodo.tipo_parametro})')

    def visitar_NombreFuncion(self, nodo):
        return self._crear_nodo(f'NombreFuncion({nodo.nombre_conjunto}, {nodo.nombre_funcion})')

    def visitar_Imprimir(self, nodo):
        id_nodo = self._crear_nodo('Imprimir')
        self._enlazador(id_nodo, nodo.argumentos_impresion)
        return id_nodo

    def visitar_ArgumentosImpresion(self, nodo):
        id_nodo = self._crear_nodo(f'ArgumentosImpresion(cadena={nodo.cadena!r})')
        for expr in nodo.operaciones_directas:
            self._enlazador(id_nodo, expr)
        return id_nodo

    def visitar_OperacionBinaria(self, nodo):
        id_nodo = self._crear_nodo(f'OperacionBinaria({nodo.operador})')
        self._enlazador(id_nodo, nodo.izquierda)
        self._enlazador(id_nodo, nodo.derecha)
        return id_nodo

    def visitar_OperacionUnaria(self, nodo):
        id_nodo = self._crear_nodo(f'OperacionUnaria({nodo.operador})')
        self._enlazador(id_nodo, nodo.derecha)
        return id_nodo

    def visitar_Variable(self, nodo):
        return self._crear_nodo(f'Variable({nodo.id})')

    def visitar_NumeroEntero(self, nodo):
        return self._crear_nodo(f'NumeroEntero({nodo.valor})')

    def visitar_NumeroFloat(self, nodo):
        return self._crear_nodo(f'NumeroFloat({nodo.valor})')
