from backend.ast_modular.impresion import Imprimir
from backend.ast_modular.match import MatchBase
from backend.arm64.generacion.tipos import es_par

def visitar_Match(self, nodo):
    """Cadena de comparaciones: cada patrón literal salta al siguiente caso si no coincide.

    `_` es el caso por defecto. Si el match se usa como expresión, el valor del brazo elegido
    queda en x0/x1; si ningún brazo coincide y no hay `_`, queda 0.
    """
    e = self.e
    n = self.nuevo_numero()
    fin = f'fin_match_{n}'
    tipo = self.tipo(nodo.expresion)
    self.visitar(nodo.expresion)
    valor = self.temporal()
    self.guardar_slot(valor, es_par(tipo), comentario='valor del match')

    for k, brazo in enumerate(nodo.brazos):
        siguiente = f'caso_match_{n}_{k + 1}'
        e.etiqueta(f'caso_match_{n}_{k}')
        if not isinstance(brazo.patron, MatchBase):
            self.visitar(brazo.patron)
            _comparar_con_patron(self, tipo, valor)
            e.instr('cbz', 'x0', siguiente)
        if isinstance(brazo.cuerpo, Imprimir):
            self.sentencia(brazo.cuerpo)
        else:
            self.visitar(brazo.cuerpo)
        e.instr('b', fin)
        if isinstance(brazo.patron, MatchBase):
            # Lo que sigue a `_` nunca se alcanza
            break
    else:
        e.etiqueta(f'caso_match_{n}_{len(nodo.brazos)}')
        e.instr('mov', 'x0', '#0', comentario='ningún brazo coincidió')
        e.instr('mov', 'x1', '#0')
    e.etiqueta(fin)

def _comparar_con_patron(self, tipo, valor):
    """Patrón en x0/x1 y valor en el temporal: deja x0 = 1 si son iguales."""
    e = self.e
    if tipo == 'String':
        e.instr('mov', 'x2', 'x0')
        e.instr('mov', 'x3', 'x1')
        self.cargar_slot(valor, True)
        e.instr('bl', 'ox_comparar_texto')
        e.instr('cmp', 'x0', '#0')
    elif tipo == 'f64':
        e.instr('fmov', 'd1', 'x0')
        self.cargar_slot(valor, False, 'x9')
        e.instr('fmov', 'd0', 'x9')
        e.instr('fcmp', 'd0', 'd1')
    else:
        self.cargar_slot(valor, False, 'x9')
        e.instr('cmp', 'x9', 'x0')
    e.instr('cset', 'x0', 'eq')
