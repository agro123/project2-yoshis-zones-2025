special_zone1 = [(0,0), (0,1), (0,2), (1,0), (2,0)]
special_zone2 = [(0,5), (0,6), (0,7), (1,7), (2,7)]
special_zone3 = [(5,0), (6,0), (7,0), (1,7), (2,7)]
special_zone4 = [(5,7), (6,7), (7,7), (7,5), (7,6)]
ZONAS = [set(special_zone1), set(special_zone2), set(special_zone3), set(special_zone4)]

def distancia_a_zona_libre(pos, estado):
    min_dist = float('inf')
    ocupadas = estado["casillas_verde"] | estado["casillas_rojo"]

    for zona in ZONAS:
        for celda in zona:
            if celda not in ocupadas:
                dx = abs(pos[0] - celda[0])
                dy = abs(pos[1] - celda[1])
                dist = dx + dy
                min_dist = min(min_dist, dist)
    return min_dist if min_dist != float('inf') else 0

def heuristica(estado):
    score = (estado["zonas_verde"] - estado["zonas_rojo"]) * 10
    score += len(estado["casillas_verde"]) - len(estado["casillas_rojo"])

    # Cercanía a meta (casilla libre en zona especial)
    dist_verde = distancia_a_zona_libre(estado["pos_verde"], estado)
    dist_rojo = distancia_a_zona_libre(estado["pos_rojo"], estado)

    # Mientras menor sea la distancia para el verde, mejor (score positivo)
    # Mientras menor sea la distancia para el rojo, peor (score negativo)
    score += (dist_rojo - dist_verde) * 0.5

    return score

"""Zonas ganadas: Se calcula la diferencia entre la cantidad de zonas especiales ganadas por el Yoshi verde y el Yoshi rojo, multiplicada por un peso alto (10). Esto refleja el objetivo principal del juego.

Casillas pintadas: Se calcula la diferencia entre la cantidad de casillas de zona ya pintadas por el Yoshi verde y el Yoshi rojo. Este factor indica la ventaja posicional parcial en zonas aún no completadas.

Proximidad a casillas por pintar: Se estima la distancia (medida como distancia Manhattan) desde la posición actual de cada Yoshi hacia la casilla más cercana no pintada de cualquier zona especial. Mientras más cerca esté el Yoshi verde y más lejos el rojo, mayor será la utilidad. Este componente anticipa oportunidades estratégicas de dominio territorial.

utilidad = (zonas_verde - zonas_rojo) * 10 \
         + (casillas_verde - casillas_rojo) \
         + (distancia_rojo - distancia_verde) * 0.5
"""