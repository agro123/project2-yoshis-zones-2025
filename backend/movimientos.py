#Todos los movimientos posibles en L
MOVIMIENTOS_CABALLO = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

def movimientos_validos(pos, casillas_ocupadas):
    movs = []
    for dx, dy in MOVIMIENTOS_CABALLO:
        x, y = pos[0] + dx, pos[1] + dy
        if 0 <= x < 8 and 0 <= y < 8 and (x, y) not in casillas_ocupadas:
            movs.append((x, y))
    return movs