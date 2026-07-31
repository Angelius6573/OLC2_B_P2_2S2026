from backend.recorrer_ast import RecorrerAST

class VisitarNodos(RecorrerAST):
    def __init__(self):
        self.nivel = 0
    def _sangria(self):
        return '  ' * self.nivel

    def visitar_Programa(self, nodo):
        print('Programa')
        self.nivel += 1
        self.visitar(nodo.declaraciones)
        self.nivel -= 1

    def visitar_DeclaracionFuncion(self, nodo):
        print(f'{self._sangria()}DeclaracionFuncion')
        self.nivel += 1
        self.visitar(nodo.nombre_funcion)
        print(f'{self._sangria()}parametros_funcion: {nodo.parametros_funcion}')
        print(f'{self._sangria()}valor_retorno: {nodo.valor_retorno}')
        self.visitar(nodo.bloque_ambito)
        self.nivel -= 1

    def visitar_NombreFuncion(self, nodo):
        print(f'{self._sangria()}NombreFuncion({nodo.nombre_conjunto}, {nodo.nombre_funcion})')

    def visitar_Imprimir(self, nodo):
        print(f'{self._sangria()}Imprimir')
        self.nivel += 1
        self.visitar(nodo.argumentos_impresion)
        self.nivel -= 1

    def visitar_ArgumentosImpresion(self, nodo):
        print(f'{self._sangria()}ArgumentosImpresion(cadena={nodo.cadena!r})')
        self.nivel += 1
        self.visitar(nodo.operaciones_directas)
        self.nivel -= 1

    def visitar_OperacionBinaria(self, nodo):
        print(f'{self._sangria()}OperacionBinaria({nodo.operador})')
        self.nivel += 1
        self.visitar(nodo.izquierda)
        self.visitar(nodo.derecha)
        self.nivel -= 1

    def visitar_OperacionUnaria(self, nodo):
        print(f'{self._sangria()}OperacionUnaria({nodo.operador})')
        self.nivel += 1
        self.visitar(nodo.derecha)
        self.nivel -= 1

    def visitar_Variable(self, nodo):
        print(f'{self._sangria()}Variable({nodo.id})')

    def visitar_NumeroEntero(self, nodo):
        print(f'{self._sangria()}NumeroEntero({nodo.valor})')

    def visitar_NumeroFloat(self, nodo):
        print(f'{self._sangria()}NumeroFloat({nodo.valor})')

    def visitar_DeclaracionStruct(self, nodo):
        print(f'{self._sangria()}DeclaracionStruct({nodo.nombre_struct})')
        self.nivel += 1
        self.visitar(nodo.parametros_struct)
        self.nivel -= 1

    def visitar_Parametros(self, nodo):
        print(f'{self._sangria()}Parametros({nodo.parametro}, {nodo.tipo_parametro})')
