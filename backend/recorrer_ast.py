class RecorrerAST:
    def visitar(self, nodo) -> str | None:
        if isinstance(nodo, list):
            for n in nodo:
                self.visitar(n)
            return
        if nodo is None:
            return
        metodo = getattr(self, f'visitar_{type(nodo).__name__}', None)
        if metodo is None:
            # Fallback genérico: cualquier nodo creado en ast_modular/ se recorre solo
            metodo = getattr(self, '_visitar_generico', None)
        if metodo is None:
            raise NotImplementedError(f'Falta visitar_{type(nodo).__name__}')
        return metodo(nodo)
