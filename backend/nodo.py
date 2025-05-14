from helpers import ZONAS, contar_zonas

class Nodo:
    def __init__(self, pos_verde=(0, 0), pos_rojo=(0, 0), casillas_verde=None, casillas_rojo=None,
            zonas_verde=0, zonas_rojo=0, padre=None, tipo='max'):
        self.padre = padre
        self.tipo = tipo  # 'max'(verde) o 'min'(rojo)
        self.profundidad = padre.profundidad + 1 if padre is not None else 0
        self.hijos = []

        self.pos_verde = pos_verde
        self.pos_rojo = pos_rojo
        self.casillas_verde = casillas_verde.copy() if casillas_verde else set()
        self.casillas_rojo = casillas_rojo.copy() if casillas_rojo else set()
        self.zonas_verde = zonas_verde
        self.zonas_rojo = zonas_rojo

        self.beta = float("inf")
        self.alfa = float("-inf")
        self.utilidad = 0

    def simular_movimiento(self, jugador, nueva_pos):
        """
        Simula el movimiento del jugador ('verde' o 'rojo') a una nueva posición,
        y retorna un nuevo estado representado como un diccionario.
        """

        nuevo_estado = {
            "pos_verde": self.pos_verde,
            "pos_rojo": self.pos_rojo,
            "casillas_verde": self.casillas_verde.copy(),
            "casillas_rojo": self.casillas_rojo.copy(),
            "zonas_verde": 0,
            "zonas_rojo": 0
        }

        # Actualiza posición
        nuevo_estado[f"pos_{jugador}"] = nueva_pos

        # Verifica si la nueva posición es parte de una zona especial
        if any(nueva_pos in zona for zona in ZONAS):
            ya_pintada = nueva_pos in nuevo_estado["casillas_verde"] or nueva_pos in nuevo_estado["casillas_rojo"]
            if not ya_pintada:
                nuevo_estado[f"casillas_{jugador}"].add(nueva_pos)

        # Recalcula zonas ganadas
        zonas_verde, zonas_rojo = contar_zonas(nuevo_estado)
        nuevo_estado["zonas_verde"] = zonas_verde
        nuevo_estado["zonas_rojo"] = zonas_rojo

        return nuevo_estado
    
    def set_alfa(self, valor):
        self.alfa = valor
    
    def set_beta(self, valor):
        self.beta = valor