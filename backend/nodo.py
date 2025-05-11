class Nodo:
    def __init__(self, pos=(0,0), padre=None, tipo='min', profundidad=0, estado=None):
        self.padre = padre
        self.tipo = tipo
        self.profundidad = profundidad
        self.pos = pos
        self.beta = None # ∞
        self.alfa = None # -∞
        self.utilidad = 0
        self.estado = estado