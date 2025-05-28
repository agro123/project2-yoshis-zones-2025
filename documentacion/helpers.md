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
