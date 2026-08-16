class SimboloVariable:
    def __init__(self, nombre, tipo, mutable, linea, columna):
        self.nombre = nombre
        self.tipo = tipo
        self.mutable = mutable
        self.linea = linea
        self.columna = columna

class SimboloFuncion:
    def __init__(self, nombre, parametros, retorno, linea, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.retorno = retorno
        self.linea = linea
        self.columna = columna

class SimboloStruct:
    def __init__(self, nombre, campos, linea, columna):
        self.nombre = nombre
        self.campos = campos
        self.linea = linea
        self.columna = columna

class TablaSimbolos:
    def __init__(self):
        self.ambitos = [{}]
        self.funciones = {}
        self.structs = {}

    def abrir_ambito(self):
        self.ambitos.append({})

    def cerrar_ambito(self):
        if len(self.ambitos) > 1:
            self.ambitos.pop()

    def ambito_actual(self):
        return self.ambitos[-1]

    def declarar_variable(self, simbolo):
        ambito = self.ambito_actual()
        if simbolo.nombre in ambito:
            return False
        ambito[simbolo.nombre] = simbolo
        return True

    def buscar_variable(self, nombre):
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                return ambito[nombre]
        return None

    def declarar_funcion(self, simbolo):
        if simbolo.nombre in self.funciones:
            return False
        self.funciones[simbolo.nombre] = simbolo
        return True

    def buscar_funcion(self, nombre):
        return self.funciones.get(nombre)

    def declarar_struct(self, simbolo):
        if simbolo.nombre in self.structs:
            return False
        self.structs[simbolo.nombre] = simbolo
        return True

    def buscar_struct(self, nombre):
        return self.structs.get(nombre)
