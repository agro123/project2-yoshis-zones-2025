from collections import deque

from nodo import Nodo
from movimientos import movimientos_validos

#Construir el arbol
def obtener_movimiento(estado_actual, dificultad):
    profundidad = {1: 2, 2: 4, 3: 6}[dificultad]
    raiz = Nodo(
        pos=estado_actual["pos_verde"],
        tipo='max',
        profundidad=0,
        estado=estado_actual
    )

    #---------Movimientos del verde---------------
    #Casillas pintadas y la posicion del rojo
    ocupadas = estado_actual["casillas_verde"] | estado_actual["casillas_rojo"] | set([estado_actual["pos_rojo"]])

    

    print(movimientos)

    queue = deque()
    stack = []
    queue.append(raiz)
    profundidad_actual = 0

    while queue:
        profundidad_actual += 1
        node: Nodo = queue.popleft()
        stack.append(node)

        movimientos = movimientos_validos(raiz.pos, ocupadas)
        for movimiento in movimientos:
            nuevo_nodo = Nodo(
                    pos=movimiento,
                    padre=node,
                    tipo='min',
                    profundidad=node.profundidad + 1,
                )

    mejor_movimiento = (0,0)

    return mejor_movimiento

def minimax(estado_actual, dificultad):
    return None
