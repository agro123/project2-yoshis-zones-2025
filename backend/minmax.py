from collections import deque
from nodo import Nodo
from helpers import movimientos_validos, ZONAS
from heuristica import heuristica


def minimax_poda(nodo: Nodo, profundidad_limite):

    #Evaluar la utilidad de las hojas
    if nodo.profundidad == profundidad_limite:
        nodo.utilidad = heuristica(nodo)
        return nodo.utilidad

    jugador = 'verde' if nodo.tipo == 'max' else 'rojo'
    posicion_actual = nodo.pos_verde if jugador == 'verde' else nodo.pos_rojo
    ocupadas = nodo.casillas_verde | nodo.casillas_rojo | {posicion_actual}
    movimientos = movimientos_validos(posicion_actual, ocupadas)

    if nodo.tipo == 'max':
        valor = float('-inf')
        for mov in movimientos:
            estado = nodo.simular_movimiento(jugador, mov)
            hijo = Nodo(
                pos_verde=estado["pos_verde"],
                pos_rojo=estado["pos_rojo"],
                casillas_verde=estado["casillas_verde"],
                casillas_rojo=estado["casillas_rojo"],
                zonas_verde=estado["zonas_verde"],
                zonas_rojo=estado["zonas_rojo"],
                padre=nodo,
                tipo='min'
            )
            nodo.hijos.append(hijo)

            hijo.set_alfa(nodo.alfa)
            hijo.set_beta(nodo.beta)

            utilidad_hijo = minimax_poda(hijo, profundidad_limite)
            valor = max(valor, utilidad_hijo)
            nodo.alfa = max(nodo.alfa, valor)

            if nodo.beta <= nodo.alfa:
                break  # Poda beta

        nodo.utilidad = valor
        return valor

    else:
        valor = float('inf')
        for mov in movimientos:
            estado = nodo.simular_movimiento(jugador, mov)
            hijo = Nodo(
                pos_verde=estado["pos_verde"],
                pos_rojo=estado["pos_rojo"],
                casillas_verde=estado["casillas_verde"],
                casillas_rojo=estado["casillas_rojo"],
                zonas_verde=estado["zonas_verde"],
                zonas_rojo=estado["zonas_rojo"],
                padre=nodo,
                tipo='max'
            )
            nodo.hijos.append(hijo)

            hijo.set_alfa(nodo.alfa)
            hijo.set_beta(nodo.beta)

            utilidad_hijo = minimax_poda(hijo, profundidad_limite)
            valor = min(valor, utilidad_hijo)
            nodo.beta = min(nodo.beta, valor)

            if nodo.beta <= nodo.alfa:
                break  # Poda alfa

        nodo.utilidad = valor

        return valor
    
def mejor_movimientov2(estado_actual, dificultad):
    profundidad = {"beginner": 2, "amateur": 4, "expert": 6}[dificultad]
    raiz = Nodo(
        pos_verde=estado_actual["pos_verde"],
        pos_rojo=estado_actual["pos_rojo"],
        casillas_verde=estado_actual["casillas_verde"],
        casillas_rojo=estado_actual["casillas_rojo"],
        zonas_verde=estado_actual["zonas_verde"],
        zonas_rojo=estado_actual["zonas_rojo"],
        tipo='max',
    )

    minimax_poda(raiz, profundidad)
    imprimir_hijos(raiz)
    mejor_utilidad = float('-inf')
    mejor_hijo = None
    for hijo in raiz.hijos:
        if hijo.utilidad > mejor_utilidad:
            mejor_utilidad = hijo.utilidad
            mejor_hijo = hijo

    return mejor_hijo.pos_verde


#Construir el arbol
def mejor_movimientov1(estado_actual, dificultad):
    profundidad = {"beginner": 2, "amateur": 4, "expert": 6}[dificultad]
    raiz = Nodo(
        pos_verde=estado_actual["pos_verde"],
        pos_rojo=estado_actual["pos_rojo"],
        casillas_verde=estado_actual["casillas_verde"],
        casillas_rojo=estado_actual["casillas_rojo"],
        zonas_verde=estado_actual["zonas_verde"],
        zonas_rojo=estado_actual["zonas_rojo"],
        tipo='max',
    )

    queue = deque()
    queue.append(raiz)
    while queue:
        node: Nodo = queue.popleft()

        if node.profundidad == profundidad:
            continue

        # Determinar jugador actual y su posición
        jugador = 'verde' if node.tipo == "max" else 'rojo'
        posicion_actual = node.pos_verde if jugador == 'verde' else node.pos_rojo

        # Calcular casillas ocupadas (incluyendo posición del nuevo nodo)
        casillas_ocupadas = node.casillas_verde | node.casillas_rojo | {posicion_actual}

        # Obtener movimientos válidos desde la posición actual
        movimientos = movimientos_validos(posicion_actual, casillas_ocupadas)
        for movimiento in movimientos:
            nuevo_estado = node.simular_movimiento(jugador, movimiento)
            nuevo_nodo = Nodo(
                    pos_verde=nuevo_estado["pos_verde"],
                    pos_rojo=nuevo_estado["pos_rojo"],
                    casillas_verde=nuevo_estado["casillas_verde"],
                    casillas_rojo=nuevo_estado["casillas_rojo"],
                    zonas_verde=nuevo_estado["zonas_verde"],
                    zonas_rojo=nuevo_estado["zonas_rojo"],
                    padre=node,
                    tipo='min' if node.tipo == "max" else 'max',
                )
            node.hijos.append(nuevo_nodo)
            queue.appendleft(nuevo_nodo)

    imprimir_hijos(raiz)
    return raiz.pos_verde

def imprimir_hijos(nodo):
        jugador = 'verde' if nodo.tipo == 'min' else 'rojo'
        pos = nodo.pos_verde if jugador == 'verde' else nodo.pos_rojo
        print(f"  Movimiento: {getattr(nodo, 'movimiento', 'N/A')}")
        print(f"  Tipo: {nodo.tipo}")
        print(f"  Posición {jugador}: {pos}")
        print(f"  Profundidad: {nodo.profundidad}")
        print(f"  Utilidad: {nodo.utilidad}")
        print("-" * 30)

        if not nodo.hijos:
            return
        else:
            for hijo in nodo.hijos:
                imprimir_hijos(hijo)

        