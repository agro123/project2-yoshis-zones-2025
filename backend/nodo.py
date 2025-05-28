from helpers import ZONAS, contar_zonas

class Nodo:

    """
    Representa un nodo del árbol de decisión en el algoritmo Minimax con poda alfa-beta
    para el juego entre dos jugadores que se mueven como caballos en un tablero 8x8.

    Cada nodo contiene el estado del juego en un punto específico de la simulación,
    incluyendo las posiciones de los jugadores, las casillas ocupadas, las zonas capturadas,
    el tipo de jugador que debe mover ('max' para el jugador verde y 'min' para el rojo),
    y los valores usados en la poda alfa-beta.

    Atributos:
        padre (Nodo | None): Nodo padre del cual se generó este estado. None si es la raíz.
        tipo (str): Tipo de nodo, 'max' si juega el verde, 'min' si juega el rojo.
        profundidad (int): Profundidad del nodo en el árbol de búsqueda.
        pos_verde (tuple): Posición actual del jugador verde (fila, columna).
        pos_rojo (tuple): Posición actual del jugador rojo (fila, columna).
        casillas_verde (set): Conjunto de celdas pintadas por el jugador verde.
        casillas_rojo (set): Conjunto de celdas pintadas por el jugador rojo.
        zonas_verde (int): Número de zonas capturadas por el jugador verde.
        zonas_rojo (int): Número de zonas capturadas por el jugador rojo.
        alfa (float): Valor alfa para la poda alfa-beta.
        beta (float): Valor beta para la poda alfa-beta.
        utilidad (float): Valor heurístico del nodo.
        mejor_mov (tuple | None): Movimiento óptimo desde este nodo.
    """

    def __init__(self, pos_verde=(0, 0), pos_rojo=(0, 0), casillas_verde=None, casillas_rojo=None,
            zonas_verde=0, zonas_rojo=0, padre=None, tipo='max'):
        self.padre = padre
        self.tipo = tipo  # 'max'(verde) o 'min'(rojo)
        self.profundidad = padre.profundidad + 1 if padre is not None else 0

        self.pos_verde = pos_verde
        self.pos_rojo = pos_rojo
        self.casillas_verde = casillas_verde.copy() if casillas_verde else set()
        self.casillas_rojo = casillas_rojo.copy() if casillas_rojo else set()
        self.zonas_verde = zonas_verde
        self.zonas_rojo = zonas_rojo

        self.beta = float("inf")
        self.alfa = float("-inf")
        self.utilidad =  float("-inf") if tipo == "max" else float("inf") 
        self.mejor_mov = None

    def simular_movimiento(self, jugador, nueva_pos):
        
        """
        Simula el movimiento de un jugador hacia una nueva posición y calcula el estado
        resultante del tablero, incluyendo las casillas pintadas y zonas dominadas.

        Args:
            jugador (str): 'verde' o 'rojo'.
            nueva_pos (tuple): Nueva posición a la que se mueve el jugador.

        Returns:
            dict: Un nuevo estado del juego con las claves:
                - "pos_verde": Nueva posición del jugador verde.
                - "pos_rojo": Nueva posición del jugador rojo.
                - "casillas_verde": Casillas pintadas por el verde.
                - "casillas_rojo": Casillas pintadas por el rojo.
                - "zonas_verde": Total de zonas capturadas por el verde.
                - "zonas_rojo": Total de zonas capturadas por el rojo.
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

    def set_utilidad(self, valor):
        self.utilidad = valor

    def set_mejor_mov(self, valor):
        self.mejor_mov = valor