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
