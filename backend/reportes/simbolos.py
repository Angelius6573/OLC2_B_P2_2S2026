from backend.reportes.formato_valor import formatear, por_defecto

def filas_simbolos(tabla, celdas):
    """Filas del reporte de la tabla de símbolos con «Valor»: el último valor de cada variable, o el valor por
    defecto de su tipo si su declaración nunca se ejecutó. Funciones y structs ya traen «—»."""
    filas = []
    for fila in tabla.reporte():
        if fila['valor'] is None:
            celda = celdas.get(fila['sym_id'])
            valor = formatear(celda.valor, fila['tipo']) if celda is not None else por_defecto(fila['tipo'])
            fila = {**fila, 'valor': valor}
        filas.append(fila)
    return filas
