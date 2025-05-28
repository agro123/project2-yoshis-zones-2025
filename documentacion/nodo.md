### `nodo.py`

Este archivo contiene la clase `Nodo`, que representa un estado del juego dentro del árbol de decisión del algoritmo Minimax con poda alfa-beta. Es fundamental para simular y evaluar los distintos movimientos posibles de los jugadores.

---

#### Clase `Nodo`

Representa un estado del juego con toda la información relevante para evaluar movimientos mediante Minimax.

##### Atributos:
- `padre (Nodo | None)`: Nodo padre desde el cual se generó el nodo actual.
- `tipo (str)`: `'max'` si es el turno del jugador verde, `'min'` si es el turno del jugador rojo.
- `profundidad (int)`: Nivel del nodo en el árbol de decisión.
- `pos_verde (tuple[int, int])`: Posición actual del jugador verde.
- `pos_rojo (tuple[int, int])`: Posición actual del jugador rojo.
- `casillas_verde (set[tuple])`: Casillas especiales capturadas por el jugador verde.
- `casillas_rojo (set[tuple])`: Casillas especiales capturadas por el jugador rojo.
- `zonas_verde (int)`: Zonas dominadas por el verde.
- `zonas_rojo (int)`: Zonas dominadas por el rojo.
- `alfa (float)`: Valor alfa para la poda alfa-beta.
- `beta (float)`: Valor beta para la poda alfa-beta.
- `utilidad (float)`: Valor heurístico del nodo.
- `mejor_mov (tuple | None)`: Movimiento considerado óptimo desde este nodo.

##### Métodos:
- `simular_movimiento(jugador: str, nueva_pos: tuple) -> dict`  
  Simula un movimiento del jugador (`"verde"` o `"rojo"`) hacia una nueva posición y retorna el nuevo estado del juego como diccionario.
- `set_alfa(valor: float)`  
  Actualiza el valor alfa del nodo.
- `set_beta(valor: float)`  
  Actualiza el valor beta del nodo.
- `set_utilidad(valor: float)`  
  Define el valor de utilidad del nodo.
- `set_mejor_mov(valor: tuple)`  
  Define el mejor movimiento hallado para este nodo.

---

### Ejemplo de uso

```python
from nodo import Nodo

# Crear el nodo raíz
raiz = Nodo(
    pos_verde=(0, 0),
    pos_rojo=(7, 7),
    casillas_verde=set(),
    casillas_rojo=set(),
    zonas_verde=0,
    zonas_rojo=0,
    tipo='max'
)

# Simular un movimiento del jugador máquina (verde)
estado_simulado = raiz.simular_movimiento("verde", (2, 1))
print(estado_simulado)
# Salida esperada:
# {
#     'pos_verde': (2, 1),
#     'pos_rojo': (7, 7),
#     'casillas_verde': {(2, 1)},
#     'casillas_rojo': set(),
#     'zonas_verde': 0,
#     'zonas_rojo': 0
# }

# Crear un nodo hijo desde el estado simulado
hijo = Nodo(
    pos_verde=estado_simulado["pos_verde"],
    pos_rojo=estado_simulado["pos_rojo"],
    casillas_verde=estado_simulado["casillas_verde"],
    casillas_rojo=estado_simulado["casillas_rojo"],
    zonas_verde=estado_simulado["zonas_verde"],
    zonas_rojo=estado_simulado["zonas_rojo"],
    padre=raiz,
    tipo='min'  # Ahora le toca al jugador rojo
)
