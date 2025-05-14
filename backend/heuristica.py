from helpers import ZONAS, MOVIMIENTOS_CABALLO
from collections import deque
from nodo import Nodo

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

    return float('inf')

def heuristica(nodo: Nodo):
    score = (nodo.zonas_verde - nodo.zonas_rojo) * 10
    score += len(nodo.casillas_verde) - len(nodo.casillas_rojo)

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