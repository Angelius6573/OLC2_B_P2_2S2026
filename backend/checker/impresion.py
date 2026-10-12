from backend.ast_modular.impresion import Imprimir

def visitar_Imprimir(self, nodo):
    args = nodo.argumentos_impresion
    operaciones = args.operaciones_directas
    es_rawstring = getattr(args, 'es_rawstring', False)
    if es_rawstring and operaciones:
        self.error(args.linea, args.columna, "println! con una cadena cruda no admite argumentos.")
    elif not es_rawstring and args.cadena:
        placeholders = args.cadena.count('{}') + args.cadena.count('{:?}')
        if placeholders != len(operaciones):
            self.error(args.linea, args.columna, f"println! tiene {placeholders} marcadores {{}} pero recibió "
                                                 f"{len(operaciones)} argumentos.")
    for operacion in operaciones:
        self.visitar(operacion)
    return None
