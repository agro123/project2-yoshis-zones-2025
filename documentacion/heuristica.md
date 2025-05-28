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


