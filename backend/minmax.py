from nodo import Nodo
from helpers import movimientos_validos
from heuristica import heuristica, heuristica2
import time

# Define la profundidad máxima de búsqueda del algoritmo Minimax según la dificultad seleccionada
DIFICULTAD = {"beginner": 2, "amateur": 4, "expert": 6}


def minimax_poda(nodo: Nodo, profundidad_limite):

    """
    Implementa el algoritmo Minimax con poda alfa-beta para calcular el valor de utilidad 
    de un nodo en un árbol de juego.

    Este algoritmo explora los movimientos posibles hasta una profundidad determinada y 
    asigna utilidades a los nodos terminales usando una función heurística. Durante la 
    exploración, se aplican podas para evitar evaluar ramas innecesarias cuando ya se 
    conoce que no afectarán la decisión óptima.

    Args:
        nodo (Nodo): Nodo actual del árbol de búsqueda, que representa un estado del juego.
        profundidad_limite (int): Profundidad máxima permitida para la exploración.

    Returns:
        float: Valor de utilidad del nodo actual, calculado a través de Minimax con poda.
    """

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

    """
    Determina el mejor movimiento posible para un jugador (maquina) a partir de un estado actual del juego,
    utilizando el algoritmo Minimax con poda alfa-beta.

    Esta función inicializa el nodo raíz con el estado actual del tablero, establece la profundidad de búsqueda
    en función del nivel de dificultad proporcionado, ejecuta el algoritmo de búsqueda y mide el tiempo
    de ejecución. Finalmente, retorna el movimiento que maximiza la utilidad para el jugador (maquina).

    Además, registra el tiempo de ejecución en un archivo CSV ("performance.csv") para facilitar análisis
    de rendimiento posteriores.

    Args:
        estado_actual (dict): Un diccionario con el estado actual del juego, que debe contener:
            - "pos_verde" (tuple): Posición actual del jugador verde en el tablero.
            - "pos_rojo" (tuple): Posición actual del jugador rojo en el tablero.
            - "casillas_verde" (set): Conjunto de casillas ya ocupadas por el jugador verde.
            - "casillas_rojo" (set): Conjunto de casillas ya ocupadas por el jugador rojo.
            - "zonas_verde" (int): Cantidad de zonas especiales capturadas por el jugador verde.
            - "zonas_rojo" (int): Cantidad de zonas especiales capturadas por el jugador rojo.

        dificultad (str): Nivel de dificultad del algoritmo, que determina la profundidad del árbol de búsqueda.
            Valores posibles:
            - "beginner": profundidad = 2
            - "amateur": profundidad = 4
            - "expert": profundidad = 6

    Returns:
        tuple: Movimiento óptimo para el jugador (maquina), representado como una tupla de coordenadas (fila, columna).
    """

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
    with open("performance.csv", "a", encoding="utf-8") as f:
                f.write(f"{profundidad}, {tiempo_ejecucion}\n")
    print(raiz.utilidad, f'======================++>', raiz.mejor_mov)
    return raiz.mejor_mov