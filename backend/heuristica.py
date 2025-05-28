from helpers import ZONAS, MOVIMIENTOS_CABALLO, obtener_cuadrante
from collections import deque
from nodo import Nodo

#distancia manhattan a una casilla de una zona no ganada
def menor_distancia_manhattan(nodo: Nodo):

    """
    Calcula la menor distancia de Manhattan desde la posición actual de un jugador
    hacia cualquier celda libre dentro de las zonas estratégicas disponibles.

    Una zona estratégica es ignorada si ya ha sido conquistada por cualquiera de los jugadores,
    es decir, si tiene al menos 3 celdas pintadas por el jugador rojo o por el verde.

    Args:
        nodo (Nodo): Estado actual del juego, que contiene:
            - nodo.pos_verde: posición actual del jugador verde (tupla (fila, columna)).
            - nodo.casillas_rojo: conjunto de coordenadas conquistadas por el jugador rojo.
            - nodo.casillas_verde: conjunto de coordenadas conquistadas por el jugador verde.

    Returns:
        float: La menor distancia de Manhattan desde la posición del jugador verde hasta
            alguna celda libre de las zonas aún no conquistadas. Si no hay zonas disponibles,
            devuelve `float('inf')`.
    """

    currPos = nodo.pos_verde
    posibles_zona = []

    for zona in ZONAS:
        celdas_pintadas_rojo = zona & nodo.casillas_rojo
        celdas_pintadas_verde = zona & nodo.casillas_verde
        if len(celdas_pintadas_rojo) >= 3:
            continue
        elif len(celdas_pintadas_verde) >=3:
            continue
        else:
            posibles_zona.append(zona)

    f, c = currPos

    if posibles_zona:
        return min(abs(f - casilla[0]) + abs(c - casilla[1]) for casilla in set().union(*posibles_zona))

    return float('inf')

#Distancia caballo a zona libre
def distancia_de_caballo_a_zona_libre(pos, nodo: Nodo):

    """
    Calcula la cantidad mínima de movimientos de caballo necesarios para que un jugador 
    (en una posición dada) llegue a una celda libre perteneciente a alguna zona especial
    que aún no haya sido conquistada (por ninguno de los jugadores).

    Una zona se considera conquistada si tiene al menos 3 casillas pintadas por el jugador 
    rojo o por el verde. Las zonas conquistadas se ignoran en el cálculo.

    Se utiliza búsqueda en anchura (BFS) para explorar todas las posibles posiciones alcanzables 
    con movimientos de caballo hasta encontrar una celda válida.

    Args:
        pos (tuple): Posición actual del jugador (fila, columna).
        nodo (Nodo): Estado actual del juego, que contiene:
            - nodo.casillas_rojo: conjunto de coordenadas ocupadas por el jugador rojo.
            - nodo.casillas_verde: conjunto de coordenadas ocupadas por el jugador verde.

    Returns:
        float: Número mínimo de movimientos de caballo para alcanzar una celda válida.
            Si no existe ninguna celda libre en zonas recuperables, retorna `float('inf')`.
    """

    ocupadas = nodo.casillas_verde | nodo.casillas_rojo
    visitadas = set()
    cola = deque()
    cola.append((pos, 0))

    while cola:
        actual, pasos = cola.popleft()
        if actual in visitadas:
            continue
        visitadas.add(actual)

        # Buscar si la posición actual pertenece a una zona "válida"
        for zona in ZONAS:
            celdas_pintadas = zona & nodo.casillas_rojo
            if len(celdas_pintadas) >= 3:
                continue  # zona perdida, no tiene sentido ir

            celdas_pintadas = zona & nodo.casillas_verde
            if len(celdas_pintadas) >= 3:
                continue  # zona ganada, no tiene sentido ir

            if actual in zona and actual not in ocupadas:
                return pasos  # celda libre en una zona aún recuperable

        # Expandir movimientos de caballo
        for dx, dy in MOVIMIENTOS_CABALLO:
            x, y = actual[0] + dx, actual[1] + dy
            if 0 <= x < 8 and 0 <= y < 8:
                cola.append(((x, y), pasos + 1))

    return float('inf')  # No hay zonas útiles accesibles

def heuristica(nodo: Nodo):
    """
    Evalúa el estado actual del tablero desde la perspectiva del jugador (maquina).

    La función considera:
    - Cantidad de casillas dominadas por el jugador
    - Distancia a zonas estratégicas
    - Cantidad de casillas pintadas

    Args:
        nodo : Estado actual del jugador.

    Returns:
        float: Valor heurístico del estado.
    """
    #Zonas ganadas
    score = (nodo.zonas_verde - nodo.zonas_rojo) * 10
    #Casillas pintadas
    score += len(nodo.casillas_verde) - len(nodo.casillas_rojo)
    #Proximidad a casillas por pintar
    dist_verde = distancia_de_caballo_a_zona_libre(nodo.pos_verde, nodo)
    dist_rojo = distancia_de_caballo_a_zona_libre(nodo.pos_rojo, nodo)

    # Penalizar si está lejos de zona libre
    if dist_verde != float('inf') and dist_rojo != float('inf'):
        score += (dist_rojo - dist_verde) * 0.5

    return score

def heuristica2(nodo: Nodo):

    """
    Una segunda versión de la heuristica, calcula la conveniencia del siguiente movimiento de un jugador(maquina).

    La función considera:
    - Zonas ganadas : Se calcula la diferencia entre la cantidad de zonas especiales ganadas por el Yoshi verde y el 
        Yoshi rojo, multiplicada por un peso alto (10). Esto refleja el objetivo principal del juego.

    - Casillas pintadas: Se calcula la diferencia entre la cantidad de casillas de zona ya pintadas por el Yoshi verde y 
        el Yoshi rojo. Este factor indica la ventaja posicional parcial en zonas aún no completadas.

    - Proximidad a casillas por pintar: Se estima la distancia (medida como distancia Manhattan) desde la posición actual 
        de cada Yoshi hacia la casilla más cercana no pintada de cualquier zona especial. Mientras más cerca esté el Yoshi verde 
        y más lejos el rojo, mayor será la utilidad. Este componente anticipa oportunidades estratégicas de dominio territorial.

    Args:
        nodo : Estado actual del jugador.

    Returns:
        Utilidad: (zonas_verde - zonas_rojo) * 10 \
         + (casillas_verde - casillas_rojo) \
         + (distancia_rojo - distancia_verde) * 0.5

    """

    utilidad = 0

    total_zonas = nodo.zonas_verde + nodo.zonas_rojo
    if total_zonas == 4:
        if nodo.zonas_verde > nodo.zonas_rojo:
            return 1000  # Victoria
        elif nodo.zonas_verde < nodo.zonas_rojo:
            return -1000  # Derrota
        else:
            return 0  # Empate

    # Zonas completadas
    utilidad += nodo.zonas_verde * 20
    utilidad -= nodo.zonas_rojo * 20  # penaliza progreso del rojo

    # Casillas pintadas
    utilidad += len(nodo.casillas_verde) * 2
    utilidad -= len(nodo.casillas_rojo) * 1.5  # penaliza rojo, menor peso

    #Cuadrantes estratégicos determina si necesario evitar o estar en un cuadrante
    cuadrante_verde = obtener_cuadrante(nodo.pos_verde)

    for zona in ZONAS:
        cuadrante_zona = obtener_cuadrante(next(iter(zona)))
        c_verde = len(zona & nodo.casillas_verde)
        c_rojo = len(zona & nodo.casillas_rojo)

        if c_rojo >= 3 or c_verde >= 3:
            if cuadrante_verde == cuadrante_zona:
                utilidad -= 10  # no hay necesidad de estar aca
        else:
            #  zona dominada parcialmente por verde
            if c_verde == 2:
                utilidad += 10
            # Dominio parcial del rojo
            if c_rojo == 2:
                utilidad -= 8

    # 4. Distancia a celda útil (verde)
    dist_verde = distancia_de_caballo_a_zona_libre(nodo.pos_verde, nodo)
    if dist_verde != float('inf'):
        utilidad -= dist_verde * 1.5

    return utilidad