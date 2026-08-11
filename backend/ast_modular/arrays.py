from backend.ast import Nodo

class AccederIndice(Nodo):
    def __init__(self, objetivo, indices):
        super().__init__()
        self.objetivo = objetivo
        self.indices = indices
