class Nodo:
    def __init__(self, pos=(0,0), padre=None, tipo='max', profundidad=0, estado=None):
        self.padre = padre
        self.tipo = tipo # 'max'(verde) o 'min'(rojo)
        self.profundidad = profundidad
        self.pos = pos
        self.beta = float("inf") # ∞
        self.alfa = float("-inf") # -∞
        self.utilidad = 0
        self.estado = estado