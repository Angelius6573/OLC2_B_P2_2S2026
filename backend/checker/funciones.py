from backend.ast_modular.funciones import LlamadaFuncion, Return
from backend.ast_modular.funciones_embebidas import FuncionEmbebida
from backend.checker.helpers import se_esperaba

def visitar_LlamadaFuncion(self, nodo):
    nombre = nodo.nombre_funcion
    simbolo = self.tabla.buscar_funcion(nombre)
    if simbolo is None:
        self.error(nodo.linea, nodo.columna, f"La función '{nombre}' utilizada no fue declarada")
        return None
    argumentos = [self.visitar(p) for p in nodo.parametros]
    if len(argumentos) != len(simbolo.parametros):
        self.error(nodo.linea, nodo.columna, f"La función '{nombre}' esperaba '{len(simbolo.parametros)}' argumentos, pero recibió '{len(argumentos)}'")
    else:
        for (_, tipo_param), tipo_arg in zip(simbolo.parametros, argumentos):
            if tipo_arg is not None and tipo_arg != tipo_param:
                se_esperaba(self, nodo, tipo_param, tipo_arg)
    nodo.tipo = simbolo.retorno
    return simbolo.retorno

def visitar_Return(self, nodo):
    if self._funcion_actual is None:
        self.error(nodo.linea, nodo.columna, "return fuera de una función")
        return None
    retorno = self._funcion_actual.retorno
    if nodo.valor is None:
        if retorno is not None:
            se_esperaba(self, nodo, retorno, 'sin valor')
        return None
    tipo_valor = self.visitar(nodo.valor)
    if tipo_valor is not None:
        if retorno is None:
            se_esperaba(self, nodo, 'sin valor de retorno', tipo_valor)
        elif tipo_valor != retorno:
            se_esperaba(self, nodo, retorno, tipo_valor)
    return None

def visitar_FuncionEmbebida(self, nodo):
    nombre = nodo.nombre
    if nombre == 'typeof':
        for argumento in nodo.argumentos:
            self.visitar(argumento)
        nodo.tipo = 'String'
        return 'String'
    if nombre == 'random':
        for argumento in nodo.argumentos:
            tipo = self.visitar(argumento)
            if tipo is not None and tipo != 'i32':
                se_esperaba(self, argumento, 'i32', tipo)
        nodo.tipo = 'i32'
        return 'i32'
    if nombre == 'len':
        tipo_objetivo = self.visitar(nodo.objetivo) if nodo.objetivo is not None else None
        if tipo_objetivo is not None and tipo_objetivo != 'String' and not tipo_objetivo.startswith('['):
            se_esperaba(self, nodo, 'String o arreglo', tipo_objetivo)
        nodo.tipo = 'i32'
        return 'i32'
    if nombre == 'push_str':
        tipo_objetivo = self.visitar(nodo.objetivo)
        if tipo_objetivo is not None and tipo_objetivo != 'String':
            se_esperaba(self, nodo, 'String', tipo_objetivo)
        for argumento in nodo.argumentos:
            self.visitar(argumento)
        return None
    if nombre in ('to_uppercase', 'to_lowercase', 'reverse', 'replace'):
        tipo_objetivo = self.visitar(nodo.objetivo)
        if tipo_objetivo is not None and tipo_objetivo != 'String':
            se_esperaba(self, nodo, 'String', tipo_objetivo)
        for argumento in nodo.argumentos:
            self.visitar(argumento)
        nodo.tipo = 'String'
        return 'String'
    if nombre == 'contains':
        tipo_objetivo = self.visitar(nodo.objetivo)
        if tipo_objetivo is not None and tipo_objetivo != 'String':
            se_esperaba(self, nodo, 'String', tipo_objetivo)
        for argumento in nodo.argumentos:
            self.visitar(argumento)
        nodo.tipo = 'bool'
        return 'bool'
    if nombre == 'split':
        tipo_objetivo = self.visitar(nodo.objetivo)
        if tipo_objetivo is not None and tipo_objetivo != 'String':
            se_esperaba(self, nodo, 'String', tipo_objetivo)
        for argumento in nodo.argumentos:
            self.visitar(argumento)
        nodo.tipo = '[String; n]'
        return '[String; n]'
    return None
