# Documentación del Backend

Bienvenido a la documentación general del backend. Aquí puedes acceder a la documentación específica de cada módulo del proyecto.

Para conocer la documentación sobre cada módulo, haz clic en el nombre correspondiente:

- [Helpers](#helpers.md)
- [Heurística](#heuristica.md)
- [Minimax](#minmax.md)
- [Nodo](#nodo.md)

# helpers.py

## Descripción general

Este archivo contiene funciones y datos auxiliares para manejar las zonas especiales del tablero y movimientos válidos de los jugadores (yoshis) en el juego.

El tablero es una matriz 8x8 con zonas especiales definidas que influyen en la jugabilidad.

---

## Zonas especiales

Se definen cuatro zonas especiales en el tablero, representadas por listas de coordenadas:

- **special_zone1:** [(0,0), (0,1), (0,2), (1,0), (2,0)]
- **special_zone2:** [(0,5), (0,6), (0,7), (1,7), (2,7)]
- **special_zone3:** [(5,0), (6,0), (7,0), (7,1), (7,2)]
- **special_zone4:** [(5,7), (6,7), (7,7), (7,5), (7,6)]

Todas estas zonas se agrupan en la lista `ZONAS` como conjuntos (`set`) para evitar posiciones repetidas.

---

## Funciones

### contar_zonas(estado)

Cuenta las zonas especiales ocupadas por cada jugador (verde y rojo).

**Parámetros:**

- `estado` (dict): Diccionario que contiene las casillas ocupadas por los jugadores en `"casillas_verde"` y `"casillas_rojo"`.

**Retorna:**

- `tuple(int, int)`: Número de zonas verdes y zonas rojas ocupadas respectivamente.

**Descripción:**

Para cada zona especial, si hay al menos 3 casillas ocupadas por un color, se incrementa el contador de zonas de ese color.

---

### obtener_cuadrante(pos)

Determina a qué cuadrante del tablero pertenece una posición dada.

**Parámetros:**

- `pos` (tuple(int, int)): Coordenadas (x, y) de la posición.

**Retorna:**

- `str`: Cuadrante al que pertenece la posición: `"Q1"`, `"Q2"`, `"Q3"` o `"Q4"`.

**Descripción:**

El tablero se divide en 4 cuadrantes de 4x4 celdas cada uno:
- Q1: x < 4 y y < 4
- Q2: x < 4 y y >= 4
- Q3: x >= 4 y y < 4
- Q4: x >= 4 y y >= 4

---

### movimientos_validos(nodo, jugador)

Calcula todas las posiciones válidas a las que el yoshi de un jugador puede moverse desde su posición actual.

**Parámetros:**

- `nodo` (Nodo): Estado actual del juego que incluye posiciones y casillas ocupadas.
- `jugador` (str): Color del jugador que se mueve, `"verde"` o `"rojo"`.

**Retorna:**

- `list[tuple[int, int]]`: Lista de coordenadas válidas para el movimiento.

**Descripción:**

- Considera las posiciones ocupadas por ambos jugadores y las zonas dominadas.
- Los movimientos válidos se basan en los movimientos típicos del caballo de ajedrez.
- Prioriza movimientos hacia casillas especiales no ocupadas, especialmente en la última jugada.

---

### movimiento_es_valido(mov, nodo)

Determina si un movimiento propuesto es válido.

**Parámetros:**

- `mov` (tuple(int, int)): Movimiento propuesto (posición destino).
- `nodo` (Nodo): Estado actual del juego.

**Retorna:**

- `bool`: `True` si el movimiento es válido, `False` si no.

**Descripción:**

- No se puede mover a casillas ya pintadas.
- No se puede volver a la posición anterior inmediata del jugador verde.
- No se puede mover dentro de zonas capturadas (con 3 o más casillas ocupadas).

---

## Constantes

### MOVIMIENTOS_CABALLO

Lista de desplazamientos válidos para un movimiento de tipo "caballo" (como en ajedrez):

```python
[
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

```

# heuristica.md

## Descripción general

Este archivo contiene funciones auxiliares para calcular distancias estratégicas y evaluar heurísticas sobre el estado del juego, que involucra zonas especiales y movimientos de tipo "caballo" en un tablero 8x8.

Se utilizan las zonas especiales definidas en `helpers.py` y movimientos válidos de caballo para determinar posiciones óptimas y evaluar estados para la inteligencia artificial.

---

## Funciones

### menor_distancia_manhattan(nodo: Nodo) -> float

Calcula la menor distancia Manhattan desde la posición actual del jugador verde hacia cualquier celda libre dentro de las zonas estratégicas no conquistadas.

- Ignora zonas que ya fueron ganadas (tienen 3 o más casillas pintadas por rojo o verde).
- Retorna la mínima distancia Manhattan a alguna celda libre de dichas zonas.
- Si no hay zonas disponibles, retorna `float('inf')`.

**Parámetros:**

- `nodo` (`Nodo`): Estado actual del juego, que incluye:
  - `pos_verde`: posición actual del jugador verde (fila, columna).
  - `casillas_rojo`: conjunto de casillas pintadas por rojo.
  - `casillas_verde`: conjunto de casillas pintadas por verde.

**Retorno:**

- `float`: menor distancia Manhattan a una casilla libre de zona estratégica, o infinito si no hay.

---

### distancia_de_caballo_a_zona_libre(pos: tuple, nodo: Nodo) -> float

Calcula la cantidad mínima de movimientos tipo "caballo" para que un jugador ubicado en `pos` alcance una celda libre en alguna zona especial aún no conquistada.

- Se ignoran zonas con 3 o más casillas pintadas por cualquiera de los jugadores.
- Utiliza búsqueda en anchura (BFS) sobre movimientos válidos de caballo.
- Si no hay celdas libres accesibles, retorna `float('inf')`.

**Parámetros:**

- `pos` (`tuple`): posición actual del jugador (fila, columna).
- `nodo` (`Nodo`): estado actual del juego con casillas ocupadas por ambos jugadores.

**Retorno:**

- `float`: número mínimo de movimientos tipo caballo para llegar a una celda válida, o infinito si no hay.

---

### heuristica(nodo: Nodo) -> float

Evalúa heurísticamente el estado actual del tablero desde la perspectiva del jugador máquina (verde).

- Considera:
  - Diferencia de zonas ganadas entre verde y rojo (ponderado x10).
  - Diferencia en número de casillas pintadas.
  - Diferencia en distancia a zonas libres (movimientos caballo).
- Penaliza o recompensa según cercanía a zonas libres y ventaja territorial.

**Parámetros:**

- `nodo` (`Nodo`): estado actual del juego.

**Retorno:**

- `float`: valor heurístico del estado (mayor es mejor para el jugador verde).

---

### heuristica2(nodo: Nodo) -> float

Versión avanzada de la heurística que evalúa la conveniencia del siguiente movimiento para la máquina.

- Considera:
  - Diferencia en número de zonas ganadas, con peso alto (x20).
  - Diferencia en casillas pintadas, con pesos 2 para verde y -1.5 para rojo.
  - Presencia en cuadrantes estratégicos para evitar estar en zonas ya conquistadas.
  - Penaliza o premia posiciones según dominio parcial de zonas.
  - Penaliza la distancia a celdas útiles (movimientos caballo).

- Retorna valores altos para estados ventajosos, valores muy altos (+1000) para victoria, muy bajos (-1000) para derrota, y 0 para empate.

**Parámetros:**

- `nodo` (`Nodo`): estado actual del juego.

**Retorno:**

- `float`: utilidad heurística del estado.

---

## Constantes usadas

- `ZONAS`: lista de conjuntos con las posiciones de las zonas especiales (importadas de `helpers`).
- `MOVIMIENTOS_CABALLO`: lista de tuplas con desplazamientos válidos de caballo en el tablero (importados de `helpers`).


# minmax.md

## Descripción general

Este módulo implementa el algoritmo Minimax con poda alfa-beta para determinar el mejor movimiento en un juego por turnos entre dos jugadores (verde y rojo). 

El algoritmo evalúa los estados del juego hasta una profundidad limitada, usando una heurística para estimar la utilidad de los estados terminales. La poda alfa-beta se usa para optimizar la búsqueda evitando evaluar ramas innecesarias.

---

## Funciones principales

### `minimax_poda(nodo: Nodo, profundidad_limite: int) -> float`

Ejecuta el algoritmo Minimax con poda alfa-beta desde un nodo dado hasta la profundidad límite.

- **Parámetros:**
  - `nodo`: instancia de la clase `Nodo` que representa el estado actual del juego.
  - `profundidad_limite`: número entero que indica la profundidad máxima a explorar en el árbol.

- **Retorna:**
  - Un valor de utilidad (`float`) que representa la evaluación heurística del nodo.

- **Comportamiento:**
  - Si el nodo está en la profundidad límite o el juego está en estado terminal (se han capturado 4 zonas en total), calcula la utilidad mediante la heurística y retorna.
  - Si es turno del jugador máximo (`tipo == 'max'`), busca el movimiento que maximice la utilidad.
  - Si es turno del jugador mínimo (`tipo == 'min'`), busca el movimiento que minimice la utilidad.
  - Aplica poda alfa-beta para optimizar la búsqueda.

---

### `obtener_mejor_movimiento(estado_actual: dict, dificultad: str) -> tuple`

Calcula el mejor movimiento para la máquina en base al estado actual del juego y el nivel de dificultad seleccionado.

- **Parámetros:**
  - `estado_actual`: diccionario que contiene el estado del juego con las siguientes claves:
    - `"pos_verde"`: tupla `(fila, columna)` con la posición del jugador verde.
    - `"pos_rojo"`: tupla `(fila, columna)` con la posición del jugador rojo.
    - `"casillas_verde"`: conjunto de posiciones ocupadas por verde.
    - `"casillas_rojo"`: conjunto de posiciones ocupadas por rojo.
    - `"zonas_verde"`: entero con la cantidad de zonas especiales capturadas por verde.
    - `"zonas_rojo"`: entero con la cantidad de zonas especiales capturadas por rojo.
  - `dificultad`: cadena que puede ser `"beginner"`, `"amateur"` o `"expert"`, que determina la profundidad de búsqueda.

- **Retorna:**
  - Tupla `(fila, columna)` que representa el mejor movimiento encontrado para el jugador máquina.

- **Comportamiento:**
  - Crea un nodo raíz con el estado actual.
  - Determina la profundidad de búsqueda basada en la dificultad.
  - Ejecuta el algoritmo Minimax con poda alfa-beta.
  - Registra el tiempo de ejecución en el archivo `performance.csv`.
  - Retorna el movimiento óptimo encontrado.

---

## Parámetros de dificultad

| Dificultad | Profundidad del algoritmo |
|------------|---------------------------|
| beginner   | 2                         |
| amateur    | 4                         |
| expert     | 6                         |

---

## Ejemplo de uso

```python
estado_actual = {
    "pos_verde": (4, 4),
    "pos_rojo": (0, 0),
    "casillas_verde": {(4, 4)},
    "casillas_rojo": {(0, 0)},
    "zonas_verde": 0,
    "zonas_rojo": 0,
}

dificultad = "amateur"

mejor_movimiento = obtener_mejor_movimiento(estado_actual, dificultad)
print(f"Mejor movimiento calculado: {mejor_movimiento}")


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

