from backend.ast_modular.impresion import Imprimir

def visitar_Imprimir(self, nodo):
    args = nodo.argumentos_impresion
    operaciones = args.operaciones_directas
    if getattr(args, 'es_rawstring', False) and operaciones:
        self.error(args.linea, args.columna, "println!: raw string no admite argumentos")
    else:
        placeholders = args.cadena.count('{}')
        if placeholders != len(operaciones):
            self.error(args.linea, args.columna, f"println!: {placeholders} placeholders, {len(operaciones)} argumentos")
    for operacion in operaciones:
        self.visitar(operacion)
    return None
