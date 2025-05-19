from collections import deque
from nodo import Nodo
from helpers import movimientos_validos, ZONAS
from heuristica import heuristica
import time

DIFICULTAD = {"beginner": 2, "amateur": 4, "expert": 6}

def minimax_poda(nodo: Nodo, profundidad_limite):

    #Evaluar la utilidad de las hojas
    if nodo.profundidad == profundidad_limite:
        nodo.utilidad = heuristica(nodo)
        print('--------->', nodo.utilidad)
        return nodo.utilidad

    jugador = 'verde' if nodo.tipo == 'max' else 'rojo'
    posicion_actual = nodo.pos_verde if jugador == 'verde' else nodo.pos_rojo
    posicion_contricante = nodo.pos_verde if jugador == 'rojo' else nodo.pos_rojo
    ocupadas = nodo.casillas_verde | nodo.casillas_rojo | {posicion_contricante}
    movimientos = movimientos_validos(posicion_actual, ocupadas)
    print('movimientos.', movimientos)
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

            hijo.set_alfa(nodo.alfa)
            hijo.set_beta(nodo.beta)

            utilidad_hijo = minimax_poda(hijo, profundidad_limite)
            if utilidad_hijo > valor:
                valor = utilidad_hijo
                nodo.mejor_mov = mov 
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
            hijo.set_alfa(nodo.alfa)
            hijo.set_beta(nodo.beta)

            utilidad_hijo = minimax_poda(hijo, profundidad_limite)
            

            if utilidad_hijo < valor:
                valor = utilidad_hijo
                nodo.mejor_mov = mov 
            
            nodo.beta = min(nodo.beta, valor)

            if nodo.beta <= nodo.alfa:
                break  # Poda alfa

        nodo.utilidad = valor

        return valor

#Construir el arbol con bfs y despues aplicar min max
def bfs_minmax(raiz: Nodo, profundidad):
    queue = deque()
    queue.append(raiz)
    while queue:
        node: Nodo = queue.popleft()

        if node.profundidad == profundidad:
            node.set_utilidad(heuristica(node))
            minimax(node)
            print('--------->', node.utilidad)
            continue

        # Determinar jugador actual y su posición
        jugador = 'verde' if node.tipo == "max" else 'rojo'
        posicion_actual = node.pos_verde if jugador == 'verde' else node.pos_rojo
        posicion_contricante = node.pos_verde if jugador == 'rojo' else node.pos_rojo

        # Calcular casillas ocupadas (incluyendo posición del nuevo nodo)
        casillas_ocupadas = node.casillas_verde | node.casillas_rojo | {posicion_contricante}

        # Obtener movimientos válidos desde la posición actual
        movimientos = movimientos_validos(posicion_actual, casillas_ocupadas)
        print('movimientos.', movimientos)
        for movimiento in reversed(movimientos):
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
            queue.appendleft(nuevo_nodo)

    return raiz

def minimax(nodo: Nodo):
    #Evaluar la utilidad de las hojas
    if nodo.profundidad == 0:
        #retornar utilidad del nodo final
        return nodo.utilidad

    padre: Nodo = nodo.padre
    if padre.tipo == 'max':
        if padre.utilidad < nodo.utilidad:
            padre.set_utilidad(nodo.utilidad)
            padre.set_mejor_mov(nodo.pos_verde)
        return minimax(padre)
    else:
        if padre.utilidad > nodo.utilidad:
            padre.set_utilidad(nodo.utilidad)
        return minimax(padre)

def obtener_mejor_movimiento(estado_actual, dificultad):
    profundidad = DIFICULTAD[dificultad]
    raiz = Nodo(
        pos_verde=estado_actual["pos_verde"],
        pos_rojo=estado_actual["pos_rojo"],
        casillas_verde=estado_actual["casillas_verde"],
        casillas_rojo=estado_actual["casillas_rojo"],
        zonas_verde=estado_actual["zonas_verde"],
        zonas_rojo=estado_actual["zonas_rojo"],
        tipo='max',
    )

    inicio = time.time() * 1000  # Tiempo inicial
    minimax_poda(raiz, profundidad)
    #bfs_minmax(raiz, profundidad)
    fin = time.time() * 1000  # Tiempo final
    tiempo_ejecucion = fin - inicio
    print('Tiempo de ejecucion: ', tiempo_ejecucion)
    print(raiz.utilidad, '=======================++>', raiz.mejor_mov)
    return raiz.mejor_mov