from nodo import Nodo
from helpers import movimientos_validos
from heuristica import heuristica, heuristica2
import time

DIFICULTAD = {"beginner": 2, "amateur": 4, "expert": 6}

def minimax_poda(nodo: Nodo, profundidad_limite):
    #Evaluar la utilidad de las hojas
    if nodo.profundidad == profundidad_limite or nodo.zonas_rojo + nodo.zonas_verde == 4:
        nodo.set_utilidad(heuristica2(nodo))
        return nodo.utilidad

    jugador = 'verde' if nodo.tipo == 'max' else 'rojo'
    movimientos = movimientos_validos(nodo, jugador)
    #print('movimientos.', movimientos)
    if nodo.tipo == 'max':
        valor = float('-inf')
        for mov in movimientos:
            """ if not movimiento_es_valido(mov, nodo):
                continue """
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
                nodo.set_mejor_mov(mov) 
            nodo.set_alfa(max(nodo.alfa, valor))

            if nodo.beta <= nodo.alfa:
                break  # Poda beta

        nodo.set_utilidad(valor)
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
                nodo.set_mejor_mov(mov) 
            
            nodo.set_beta(min(nodo.beta, valor))

            if nodo.beta <= nodo.alfa:
                break  # Poda alfa

        nodo.set_utilidad(valor)

        return valor

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
    with open("analisis.csv", "a", encoding="utf-8") as f:
                f.write(f"{profundidad}, {tiempo_ejecucion}\n")
    print(raiz.utilidad, f'======================++>', raiz.mejor_mov)
    return raiz.mejor_mov