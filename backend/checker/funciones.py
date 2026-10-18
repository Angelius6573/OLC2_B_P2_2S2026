from backend.ast_modular.funciones import LlamadaFuncion, Return
from backend.ast_modular.funciones_embebidas import FuncionEmbebida
from backend.ast_modular.aritmetica import Variable
from backend.ast_modular.arrays import AccederIndice
from backend.checker.helpers import se_esperaba, inmutable, tipo_elemento

def _variable_receptora(objetivo):
    # s.push_str(...) modifica s; m[i].push_str(...) modifica m
    while isinstance(objetivo, AccederIndice):
        objetivo = objetivo.objetivo
    return objetivo if isinstance(objetivo, Variable) else None

def visitar_LlamadaFuncion(self, nodo):
    nombre = nodo.nombre_funcion
    simbolo = self.tabla.buscar_funcion(nombre)
    if simbolo is None:
        self.error(nodo.linea, nodo.columna, f"La función '{nombre}' no ha sido declarada.")
        return None
    argumentos = [self.visitar(p) for p in nodo.parametros]
    if len(argumentos) != len(simbolo.parametros):
        self.error(nodo.linea, nodo.columna, f"La función '{nombre}' esperaba {len(simbolo.parametros)} argumentos, "
                                             f"pero recibió {len(argumentos)}.")
    else:
        for (_, tipo_param), tipo_arg in zip(simbolo.parametros, argumentos):
            if tipo_arg is not None and tipo_arg != tipo_param:
                se_esperaba(self, nodo, tipo_param, tipo_arg)
    nodo.tipo = simbolo.retorno
    return simbolo.retorno

def visitar_Return(self, nodo):
    if self._funcion_actual is None:
        self.error(nodo.linea, nodo.columna, "La sentencia return está fuera de una función.")
        return None
    retorno = self._funcion_actual.retorno
    funcion = self._funcion_actual.nombre
    if nodo.valor is None:
        if retorno is not None:
            self.error(nodo.linea, nodo.columna, f"La función '{funcion}' debe devolver un valor de tipo {retorno}.")
        return None
    tipo_valor = self.visitar(nodo.valor)
    if tipo_valor is not None:
        if retorno is None:
            self.error(nodo.linea, nodo.columna,
                       f"La función '{funcion}' no declara tipo de retorno, pero devuelve un valor de tipo {tipo_valor}.")
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
        # Un String solo crece si su variable se declaró con mut
        receptora = _variable_receptora(nodo.objetivo)
        simbolo = self.tabla.buscar_variable(receptora.id) if receptora is not None else None
        if simbolo is not None and not simbolo.mutable:
            inmutable(self, nodo, receptora.id)
        for argumento in nodo.argumentos:
            tipo_argumento = self.visitar(argumento)
            if tipo_argumento is not None and tipo_argumento != 'String':
                se_esperaba(self, argumento, 'String', tipo_argumento)
        return None
    if nombre in ('to_uppercase', 'to_lowercase', 'replace'):
        tipo_objetivo = self.visitar(nodo.objetivo)
        if tipo_objetivo is not None and tipo_objetivo != 'String':
            se_esperaba(self, nodo, 'String', tipo_objetivo)
        for argumento in nodo.argumentos:
            self.visitar(argumento)
        nodo.tipo = 'String'
        return 'String'
    if nombre == 'reverse':
        tipo_objetivo = self.visitar(nodo.objetivo)
        if tipo_objetivo is not None and tipo_objetivo != 'String' and not tipo_objetivo.startswith('['):
            se_esperaba(self, nodo, 'String o arreglo', tipo_objetivo)
        for argumento in nodo.argumentos:
            self.visitar(argumento)
        nodo.tipo = tipo_objetivo
        return tipo_objetivo
    if nombre == 'contains':
        tipo_objetivo = self.visitar(nodo.objetivo)
        tipo_argumento = self.visitar(nodo.argumentos[0])
        if tipo_objetivo is not None and tipo_objetivo != 'String' and not tipo_objetivo.startswith('['):
            se_esperaba(self, nodo, 'String o arreglo', tipo_objetivo)
        elif tipo_objetivo is not None and tipo_argumento is not None:
            # En un String se busca otro String; en un arreglo, un valor del tipo de sus elementos
            esperado = 'String' if tipo_objetivo == 'String' else tipo_elemento(tipo_objetivo)
            if tipo_argumento != esperado:
                se_esperaba(self, nodo.argumentos[0], esperado, tipo_argumento)
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
