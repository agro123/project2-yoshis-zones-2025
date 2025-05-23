#[
#    [1, 1, 1, 0, 0, 1, 1, 1],
#    [1, 0, 0, 0, 0, 0, 0, 1],
#    [1, 0, 0, 0, 0, 0, 0, 1],
#    [0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0],
#    [1, 0, 0, 0, 0, 0, 0, 1],
#    [1, 0, 0, 0, 0, 0, 0, 1],
#    [1, 1, 1, 0, 0, 1, 1, 1]
#]

special_zone1 = [(0,0), (0,1), (0,2), (1,0), (2,0)]
special_zone2 = [(0,5), (0,6), (0,7), (1,7), (2,7)]
special_zone3 = [(5,0), (6,0), (7,0), (1,7), (2,7)]
special_zone4 = [(5,7), (6,7), (7,7), (7,5), (7,6)]

ZONAS = [set(special_zone1), set(special_zone2), set(special_zone3), set(special_zone4)]

#Recuenta cuántas zonas ha ganado cada jugador.
def contar_zonas(estado):
    zonas_verde = zonas_rojo = 0
    for zona in ZONAS:
        c_verde = len(zona & estado["casillas_verde"])
        c_rojo = len(zona & estado["casillas_rojo"])

        if c_verde >= 3:
            zonas_verde += 1
        elif c_rojo >= 3:
            zonas_rojo += 1

    return zonas_verde, zonas_rojo

#Todos los movimientos posibles en L
MOVIMIENTOS_CABALLO = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

def movimientos_validos(pos, casillas_ocupadas, casillas_verde, casillas_rojo):
    movs = []
    casillas_pintadas = casillas_verde | casillas_rojo

    zonas_ocupadas = set()
    for zona in ZONAS:
        zonas_ocupadas |= (zona & casillas_pintadas)

    for dx, dy in MOVIMIENTOS_CABALLO:
        x, y = pos[0] + dx, pos[1] + dy
        if 0 <= x < 8 and 0 <= y < 8 \
            and (x, y) not in casillas_ocupadas \
            and (x, y) not in zonas_ocupadas:
            movs.append((x, y))
    return movs

def movimiento_es_valido(mov, estado):
    casillas_pintadas = estado["casillas_verde"] | estado["casillas_rojo"]

    # Si la casilla ya está pintada, no es válida
    if mov in casillas_pintadas:
        return False

    # Si pertenece a una zona capturada (3 o más celdas pintadas por alguien), tampoco es válida
    for zona in ZONAS:
        c_verde = len(zona & estado["casillas_verde"])
        c_rojo = len(zona & estado["casillas_rojo"])
        if c_verde >= 3 or c_rojo >= 3:
            if mov in zona:
                return False
    return True
