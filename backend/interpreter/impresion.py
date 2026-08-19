from backend.ast_modular.impresion import Imprimir, ArgumentosImpresion

def visitar_Imprimir(self, nodo):
    args = nodo.argumentos_impresion
    cadena = args.cadena
    operaciones = args.operaciones_directas
    if operaciones:
        valores = [str(self.visitar(op)) for op in operaciones]
        resultado = cadena
        for val in valores:
            resultado = resultado.replace('{}', val, 1)
        print(resultado)
    else:
        print(cadena)
    return None
