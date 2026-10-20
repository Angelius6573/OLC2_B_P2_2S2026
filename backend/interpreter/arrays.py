from backend.ast_modular.arrays import AccederIndice, AsignarIndice, Slice, Repetidor

def visitar_AccederIndice(self, nodo):
    objetivo = self.visitar(nodo.objetivo)
    actual = objetivo
    for indice in nodo.indices:
        idx = self.visitar(indice)
        if isinstance(actual, list) and isinstance(idx, int):
            if 0 <= idx < len(actual):
                actual = actual[idx]
            else:
                raise RuntimeError(f"{nodo.linea}:{nodo.columna} Índice fuera de rango")
        else:
            raise RuntimeError(f"{nodo.linea}:{nodo.columna} No se puede indexar")
    return actual

def visitar_AsignarIndice(self, nodo):
    acceder = nodo.objetivo
    contenedor = self.visitar(acceder.objetivo)
    for indice in acceder.indices[:-1]:
        idx = self.visitar(indice)
        if isinstance(contenedor, list) and isinstance(idx, int):
            if 0 <= idx < len(contenedor):
                contenedor = contenedor[idx]
            else:
                raise RuntimeError(f"{nodo.linea}:{nodo.columna} Índice fuera de rango")
        else:
            raise RuntimeError(f"{nodo.linea}:{nodo.columna} No se puede indexar")
    ultimo_idx = self.visitar(acceder.indices[-1])
    valor = self.visitar(nodo.valor)
    if isinstance(contenedor, list) and isinstance(ultimo_idx, int):
        if 0 <= ultimo_idx < len(contenedor):
            contenedor[ultimo_idx] = valor
        else:
            raise RuntimeError(f"{nodo.linea}:{nodo.columna} Índice fuera de rango")
    else:
        raise RuntimeError(f"{nodo.linea}:{nodo.columna} No se puede asignar índice")
    return None

def visitar_Slice(self, nodo):
    objetivo = self.visitar(nodo.objetivo)
    inicio = self.visitar(nodo.inicio) if nodo.inicio else 0
    fin = self.visitar(nodo.fin) if nodo.fin else len(objetivo)
    if isinstance(objetivo, (list, str)):
        # Como en ARM64: Python recortaría el rango sin avisar
        if not 0 <= inicio <= fin <= len(objetivo):
            raise RuntimeError(f"{nodo.linea}:{nodo.columna} Índice fuera de rango")
        return objetivo[inicio:fin]
    raise RuntimeError(f"{nodo.linea}:{nodo.columna} No se puede hacer slice")

def visitar_Repetidor(self, nodo):
    valor = self.visitar(nodo.valor)
    cantidad = self.visitar(nodo.cantidad)
    if isinstance(cantidad, int) and cantidad >= 0:
        return [valor] * cantidad
    raise RuntimeError(f"{nodo.linea}:{nodo.columna} Cantidad inválida para repetidor")
