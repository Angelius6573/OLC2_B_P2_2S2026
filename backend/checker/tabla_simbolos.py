AMBITO_GLOBAL = 'Global'
SIN_VALOR = '—'

class SimboloVariable:
    def __init__(self, nombre, tipo, mutable, linea, columna, categoria='Variable'):
        self.nombre = nombre
        self.tipo = tipo
        self.mutable = mutable
        self.linea = linea
        self.columna = columna
        self.categoria = categoria
        # Los asigna TablaSimbolos.declarar_variable
        self.sym_id = None
        self.ambito = None
        # Offset del slot en el marco de su función; lo llena el generador ARM64
        self.offset = None

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
        # Nombre de la función que se analiza; da la columna «Ámbito» del reporte
        self.ambito_nombre = AMBITO_GLOBAL
        # Los diccionarios de `ambitos` se vacían al cerrarse; estos registros no
        self.simbolos = []
        self.variables_por_sym_id = {}
        self._siguiente_sym_id = 1

    def abrir_ambito(self):
        self.ambitos.append({})

    def cerrar_ambito(self):
        if len(self.ambitos) > 1:
            self.ambitos.pop()

    def ambito_actual(self):
        return self.ambitos[-1]

    def declarar_variable(self, simbolo):
        # Cada declaración recibe un sym_id nuevo, también si sombrea a otra con el mismo nombre
        simbolo.sym_id = self._siguiente_sym_id
        simbolo.ambito = self.ambito_nombre
        self._siguiente_sym_id += 1
        self.variables_por_sym_id[simbolo.sym_id] = simbolo
        self.simbolos.append(simbolo)
        self.ambito_actual()[simbolo.nombre] = simbolo
        return True

    def buscar_variable(self, nombre):
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                return ambito[nombre]
        return None

    def variables_de(self, funcion):
        return [s for s in self.variables_por_sym_id.values() if s.ambito == funcion]

    def declarar_funcion(self, simbolo):
        if simbolo.nombre in self.funciones:
            return False
        self.funciones[simbolo.nombre] = simbolo
        self.simbolos.append(simbolo)
        return True

    def buscar_funcion(self, nombre):
        return self.funciones.get(nombre)

    def declarar_struct(self, simbolo):
        if simbolo.nombre in self.structs:
            return False
        self.structs[simbolo.nombre] = simbolo
        self.simbolos.append(simbolo)
        return True

    def buscar_struct(self, nombre):
        return self.structs.get(nombre)

    def reporte(self):
        """Filas del reporte de símbolos, en orden de registro.

        Funciones y structs se registran antes de visitar cualquier cuerpo, así que van
        primero. La columna «Valor» de una variable queda en None: la llena el intérprete.
        """
        filas = []
        for no, simbolo in enumerate(self.simbolos, start=1):
            if isinstance(simbolo, SimboloVariable):
                fila = {
                    'categoria': simbolo.categoria,
                    'tipo': simbolo.tipo if simbolo.tipo is not None else SIN_VALOR,
                    'ambito': simbolo.ambito,
                    'valor': None,
                    'sym_id': simbolo.sym_id,
                }
            elif isinstance(simbolo, SimboloFuncion):
                fila = {
                    'categoria': 'Función',
                    'tipo': simbolo.retorno if simbolo.retorno is not None else '()',
                    'ambito': AMBITO_GLOBAL,
                    'valor': SIN_VALOR,
                    'sym_id': None,
                }
            else:
                fila = {
                    'categoria': 'Struct',
                    'tipo': simbolo.nombre,
                    'ambito': AMBITO_GLOBAL,
                    'valor': SIN_VALOR,
                    'sym_id': None,
                }
            filas.append({
                'no': no,
                'identificador': simbolo.nombre,
                'categoria': fila['categoria'],
                'tipo': fila['tipo'],
                'ambito': fila['ambito'],
                'linea': simbolo.linea,
                'valor': fila['valor'],
                'sym_id': fila['sym_id'],
            })
        return filas
