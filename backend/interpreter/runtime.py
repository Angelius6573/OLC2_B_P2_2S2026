class _ReturnValue(Exception):
    def __init__(self, valor):
        self.valor = valor

class _BreakSignal(Exception):
    def __init__(self, label=None):
        self.label = label

class _ContinueSignal(Exception):
    pass

class Variable:
    __slots__ = ('valor', 'mutable')
    def __init__(self, valor, mutable=False):
        self.valor = valor
        self.mutable = mutable

class Funcion:
    __slots__ = ('parametros', 'bloque', 'retorno')
    def __init__(self, parametros, bloque, retorno=None):
        self.parametros = parametros
        self.bloque = bloque
        self.retorno = retorno

class StructDef:
    __slots__ = ('campos',)
    def __init__(self, campos):
        self.campos = campos

class InstanciaStruct:
    __slots__ = ('campos',)
    def __init__(self, campos):
        self.campos = campos

class Ambito:
    __slots__ = ('variables', 'padre')
    def __init__(self, padre=None):
        self.variables = {}
        self.padre = padre

    def declarar(self, nombre, valor, mutable=False):
        self.variables[nombre] = Variable(valor, mutable)

    def asignar(self, nombre, valor):
        if nombre in self.variables:
            v = self.variables[nombre]
            if not v.mutable:
                raise RuntimeError(f"Variable '{nombre}' no es mutable")
            v.valor = valor
            return True
        if self.padre is not None:
            return self.padre.asignar(nombre, valor)
        return False

    def buscar(self, nombre):
        if nombre in self.variables:
            return self.variables[nombre]
        if self.padre is not None:
            return self.padre.buscar(nombre)
        return None
