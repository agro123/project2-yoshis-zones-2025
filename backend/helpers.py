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

"""
Zonas especiales en todo el mapa, estas serán utilizadas para calcular el momento en el que una de estas estan ocupadas o van a 
ser ocupadas por un jugador
"""
special_zone1 = [(0,0), (0,1), (0,2), (1,0), (2,0)]
special_zone2 = [(0,5), (0,6), (0,7), (1,7), (2,7)]
special_zone3 = [(5,0), (6,0), (7,0), (7,1), (7,2)]
special_zone4 = [(5,7), (6,7), (7,7), (7,5), (7,6)]

""" Guarda en general todas las posiciones especiales del tablero, usa set para evitar posiciones repetidas """
ZONAS = [set(special_zone1), set(special_zone2), set(special_zone3), set(special_zone4)]


def contar_zonas(estado):
    """
    Cuenta las conas especiales tanto rojas como verdes que han sido ocupadas ya.

    Args:
        estado dict[string]  : Diccionario que contiene información sobre el estado actual de las casillas de cada color

    Returns:
        tuple(int,int) : Tupla con el calculo de conteo de las zonas verdes y zonas rojas respectivamente
    
    """
    zonas_verde = zonas_rojo = 0
    for zona in ZONAS:
        c_verde = len(zona & estado["casillas_verde"])
        c_rojo = len(zona & estado["casillas_rojo"])

        if c_verde >= 3:
            zonas_verde += 1
        elif c_rojo >= 3:
            zonas_rojo += 1

    return zonas_verde, zonas_rojo

""" Estos son todos los movimientos que un yoshi es capaz de hacer, al sumar estas coordenadas a la posición actual del yoshi
se puede calcular su movimiento """

MOVIMIENTOS_CABALLO = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

def obtener_cuadrante(pos):

    """
    El tablaro esta dividido en 4 cuadrantes, esta función permite calcular a partir de la posición el cuadrante en el que se encuentra
    un jugador en un momento dado.

    Args:
        pos tuple(int,int) : posición del jugador a la que se quiere calcular el cuadrante
    
    Returns:
        Cuadrante al que pertenece ("Q1","Q2","Q3","Q4")
    
    """

    x, y = pos
    if x < 4 and y < 4:
        return 'Q1'
    elif x < 4 and y >= 4:
        return 'Q2'
    elif x >= 4 and y < 4:
        return 'Q3'
    else:
        return 'Q4'

def movimientos_validos(nodo, jugador):

    """
    Genera todas las posiciones válidas a las que se puede mover un yoshi desde una posición dada en el tablero.

    Args:
        Nodo: Posición actual del jugador (x, y).
        jugador: color actual del yoshi a moverse

    Returns:
        list[tuple[int, int]]: Lista de coordenadas válidas que el caballo puede alcanzar desde la posición dada.
    """
     
    posicion_actual = nodo.pos_verde if jugador == 'verde' else nodo.pos_rojo
    posicion_contricante = nodo.pos_verde if jugador == 'rojo' else nodo.pos_rojo
    casillas_ocupadas = nodo.casillas_verde | nodo.casillas_rojo | {posicion_contricante}

    zonas_ocupadas = set()
    casillas_pintadas = nodo.casillas_verde | nodo.casillas_rojo

    movs = []
    movs_better = []

    es_ultima_jugada = nodo.zonas_verde + nodo.zonas_rojo == 3

    #Zonas ya dominandas
    for zona in ZONAS:
        c_verde = len(zona & nodo.casillas_verde)
        c_rojo = len(zona & nodo.casillas_rojo)
        if c_verde >= 3 or c_rojo >= 3:
            zonas_ocupadas |= zona

    for dx, dy in MOVIMIENTOS_CABALLO:
        x, y = posicion_actual[0] + dx, posicion_actual[1] + dy
        not_here = (x,y) not in casillas_ocupadas and (x, y) not in zonas_ocupadas

        if jugador == 'verde' and es_ultima_jugada and (x,y) in set().union(*ZONAS) - zonas_ocupadas and not_here: 
            movs_better.append((x,y))
            continue
        if jugador == 'verde' and (x,y) in set().union(*ZONAS) - casillas_pintadas and not_here:
            movs_better.append((x,y))
            continue

        if 0 <= x < 8 and 0 <= y < 8 \
            and not_here:
            movs.append((x, y))

    if movs_better:
        return movs_better
    return movs

def movimiento_es_valido(mov, nodo):

    """
    Calcula si un movimiento de un yoshi es valido hacia alguna de las casillas especiales, es decir, si un movimiento de un yoshi
    esta dirigido hacia una casilla especial ya ocupada entonces no puede ser contado como una casilla pintada por ese jugador

    Args:
        mov: es el movimiento al que se quiere calcular su validez
        nodo: estado actual del jugador

    Returns:
        True si es un movimiento valido, False si no es posible este movimiento
    
    """

    casillas_pintadas = nodo.casillas_verde | nodo.casillas_rojo

    # Si la casilla ya está pintada, no es válida
    if mov in casillas_pintadas:
        return False
    
    padre = nodo.padre
    while padre and padre.profundidad != 0:
        padre = padre.padre
    
    if padre and mov == padre.pos_verde:
        return False
    # Si pertenece a una zona capturada (3 o más celdas pintadas por alguien), tampoco es válida
    for zona in ZONAS:
        c_verde = len(zona & nodo.casillas_verde)
        c_rojo = len(zona & nodo.casillas_rojo)
        if c_verde >= 3 or c_rojo >= 3:
            if mov in zona:
                return False
    return True