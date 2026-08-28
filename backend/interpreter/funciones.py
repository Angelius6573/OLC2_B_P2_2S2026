from backend.ast_modular.funciones import LlamadaFuncion, Return
from backend.ast_modular.funciones_embebidas import FuncionEmbebida
from backend.ast_modular.aritmetica import Variable
from backend.interpreter.runtime import _ReturnValue, Funcion, InstanciaStruct, Ambito

def visitar_LlamadaFuncion(self, nodo):
    nombre = nodo.nombre_funcion
    argumentos = [self.visitar(p) for p in nodo.parametros]
    return self._llamar_funcion(nombre, argumentos)

def _llamar_funcion(self, nombre, argumentos):
    if nombre in self._funciones_embebidas:
        return self._funciones_embebidas[nombre](argumentos)
    func = self.funciones.get(nombre)
    if func is None:
        raise RuntimeError(f"Función '{nombre}' no declarada")
    nuevo = Ambito(self.ambito_actual)
    for i, (nombre_param, _) in enumerate(func.parametros):
        valor = argumentos[i] if i < len(argumentos) else None
        nuevo.declarar(nombre_param, valor)
    anterior = self.ambito_actual
    self.ambito_actual = nuevo
    try:
        for instruccion in func.bloque:
            self.visitar(instruccion)
        return None
    except _ReturnValue as rv:
        return rv.valor
    finally:
        self.ambito_actual = anterior

def visitar_Return(self, nodo):
    valor = self.visitar(nodo.valor) if nodo.valor is not None else None
    raise _ReturnValue(valor)

def visitar_FuncionEmbebida(self, nodo):
    nombre = nodo.nombre
    argumentos = [self.visitar(a) for a in nodo.argumentos]
    objetivo = self.visitar(nodo.objetivo) if nodo.objetivo is not None else None
    resultado = _ejecutar_embebida(self, nombre, objetivo, argumentos, nodo)
    if isinstance(nodo.objetivo, Variable) and nombre in ('push_str', 'reverse'):
        var_nombre = nodo.objetivo.id
        v = self.ambito_actual.buscar(var_nombre)
        if v is not None:
            v.valor = resultado
    return resultado

def _ejecutar_embebida(self, nombre, objetivo, argumentos, nodo):
    if nombre == 'typeof':
        return _typeofvalor(argumentos[0] if argumentos else None)
    if nombre == 'random':
        import random
        if len(argumentos) == 2:
            return random.randint(argumentos[0], argumentos[1])
        if len(argumentos) == 1:
            return random.randint(0, argumentos[0])
        return random.randint(0, 100)
    if nombre == 'len':
        obj = objetivo if objetivo is not None else (argumentos[0] if argumentos else None)
        if isinstance(obj, str):
            return len(obj)
        if isinstance(obj, list):
            return len(obj)
        return 0
    if nombre == 'push_str':
        if isinstance(objetivo, str) and argumentos:
            return objetivo + str(argumentos[0])
        return objetivo
    if nombre == 'to_uppercase':
        return objetivo.upper() if isinstance(objetivo, str) else objetivo
    if nombre == 'to_lowercase':
        return objetivo.lower() if isinstance(objetivo, str) else objetivo
    if nombre == 'reverse':
        if isinstance(objetivo, (str, list)):
            return objetivo[::-1]
        return objetivo
    if nombre == 'replace':
        if isinstance(objetivo, str) and len(argumentos) >= 2:
            return objetivo.replace(str(argumentos[0]), str(argumentos[1]))
        return objetivo
    if nombre == 'contains':
        return str(argumentos[0]) in objetivo if isinstance(objetivo, str) and argumentos else False
    if nombre == 'split':
        return objetivo.split(str(argumentos[0])) if isinstance(objetivo, str) and argumentos else [objetivo] if objetivo is not None else []
    return None

def _typeofvalor(val):
    if val is None:
        return 'null'
    if isinstance(val, bool):
        return 'bool'
    if isinstance(val, int):
        return 'i32'
    if isinstance(val, float):
        return 'f64'
    if isinstance(val, str):
        return 'String'
    if isinstance(val, list):
        return 'Array'
    if isinstance(val, InstanciaStruct):
        return 'Struct'
    return 'unknown'
