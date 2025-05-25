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

def heuristica(nodo: Nodo):
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
    distancia = menor_distancia_caballo(nodo)
    print(f"Distancia ====> {nodo.pos_verde} {distancia}")
    utilidad -= distancia

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