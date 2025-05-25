from helpers import ZONAS, MOVIMIENTOS_CABALLO, movimiento_es_valido
from collections import deque
from nodo import Nodo

#distancia caballo a una casilla de una zona no ganada
def menor_distancia_caballo(nodo: Nodo):
    currPos = nodo.pos_verde
    casillas_destino = set().union(*ZONAS)

    if currPos in casillas_destino:
        return 0

    posibles_casillas = []
    for casilla in casillas_destino:
        if movimiento_es_valido(
            nodo.pos_verde,
            {"casillas_verde": nodo.casillas_verde, "casillas_rojo": nodo.casillas_rojo}
        ):
            posibles_casillas.append(casilla)

    visitado = set()
    cola = deque([(currPos, 0)])

    while cola:
        (x, y), dist = cola.popleft()
        if (x, y) in posibles_casillas:
            return dist
        for dx, dy in MOVIMIENTOS_CABALLO:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in visitado and (0 <= nx < 8 and 0 <= ny < 8):  # Asumiendo tablero 8x8
                visitado.add((nx, ny))
                cola.append(((nx, ny), dist + 1))

    return float('inf')

#distancia manhattan a una casilla de una zona no ganada
def menor_distancia_manhattan(nodo: Nodo):
    currPos = nodo.pos_verde
    casillas = set().union(*ZONAS)
    posibles_casillas = []

    if currPos in casillas:
        return 0

    for casilla in casillas:
        if movimiento_es_valido(nodo.pos_verde, {"casillas_verde": nodo.casillas_verde, "casillas_rojo": nodo.casillas_rojo}):
            posibles_casillas.append(casilla)

    f, c = currPos

    return min(abs(f - casilla[0]) + abs(c - casilla[1]) for casilla in posibles_casillas)

def distancia_de_caballo_a_zona_libre(pos, nodo: Nodo):
    ocupadas = nodo.casillas_verde | nodo.casillas_rojo
    visitadas = set()
    cola = deque()
    cola.append((pos, 0))

    while cola:
        actual, pasos = cola.popleft()
        if actual in visitadas:
            continue
        visitadas.add(actual)

        for zona in ZONAS:
            for celda in zona:
                if celda == actual and celda not in ocupadas:
                    return pasos  # ya llegaste

        for dx, dy in MOVIMIENTOS_CABALLO:
            x, y = actual[0] + dx, actual[1] + dy
            if 0 <= x < 8 and 0 <= y < 8:
                cola.append(((x, y), pasos + 1))


def heuristica(nodo: Nodo):
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

"""Zonas ganadas: Se calcula la diferencia entre la cantidad de zonas especiales ganadas por el Yoshi verde y el Yoshi rojo, multiplicada por un peso alto (10). Esto refleja el objetivo principal del juego.

Casillas pintadas: Se calcula la diferencia entre la cantidad de casillas de zona ya pintadas por el Yoshi verde y el Yoshi rojo. Este factor indica la ventaja posicional parcial en zonas aún no completadas.

Proximidad a casillas por pintar: Se estima la distancia (medida como distancia Manhattan) desde la posición actual de cada Yoshi hacia la casilla más cercana no pintada de cualquier zona especial. Mientras más cerca esté el Yoshi verde y más lejos el rojo, mayor será la utilidad. Este componente anticipa oportunidades estratégicas de dominio territorial.

utilidad = (zonas_verde - zonas_rojo) * 10 \
         + (casillas_verde - casillas_rojo) \
         + (distancia_rojo - distancia_verde) * 0.5
"""


def heuristica2(nodo: Nodo):
    utilidad = 0

    # Se completan mas zonas que rojo
    if nodo.zonas_verde + nodo.zonas_rojo == 4 and nodo.zonas_verde > nodo.zonas_rojo:
        return float('inf')  #Si se completan mas zonas que rojo
    
    """     if nodo.zonas_verde + nodo.zonas_rojo == 4 and nodo.zonas_rojo > nodo.zonas_verde:
        return float('-inf')  #Si se completan mas zonas que rojo
    
    if nodo.zonas_verde + nodo.zonas_rojo == 4 and nodo.zonas_rojo == nodo.zonas_verde:
        return 0 #Si se empata """
    
    # Se completa una zona
    if nodo.zonas_verde > nodo.padre.zonas_verde:
        utilidad += 10
    
    # Se completa una casilla en una zona especial
    if len(nodo.casillas_verde) > len(nodo.padre.casillas_verde):
        utilidad += 5
    
    # distancia a una casilla libre
    distancia = menor_distancia_manhattan(nodo)
    print(f"Distancia ====> {nodo.pos_verde} {distancia}")
    #utilidad -= distancia

    return utilidad


"""
1. Si se completan mas zonas que rojo
2. Si se completa una zona un valor positivo alto
3. Si se completa una casilla en una zona especial un positivo medio
3.5 distancia caballo 
4. Si se empata en zonas  0
5. Si se acerca a una casilla por pintar un valor negativo bajo
7. Si se aleja de la casilla por pintar un valor negativo alto
6. Si se completa menos zonas que rojo
"""