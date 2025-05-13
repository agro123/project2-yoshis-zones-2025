# Yoshi’s Zones

Juego desarrollado como Proyecto 2 para la asignatura de **Inteligencia Artificial** en la Universidad del Valle.

## 🕹️ Descripción del juego

**Yoshi’s Zones** es un juego por turnos entre dos adversarios: un jugador humano y una IA. Cada uno controla un personaje Yoshi (verde o rojo) que se mueve como un **caballo** en el ajedrez. El objetivo del juego es **ganar la mayoría de las zonas especiales** en el tablero.

### 🎯 Objetivo
Ganar más zonas especiales que el oponente. Una zona es ganada cuando un Yoshi pinta la mayoría de sus 5 casillas.

---

## 📋 Reglas del juego

- Cada jugador mueve su Yoshi como un caballo de ajedrez.
- Las **zonas especiales** están en cada esquina del tablero y constan de 5 casillas.
- Al moverse a una casilla de zona especial, esta se pinta del color del jugador.
- Las casillas pintadas no se pueden volver a usar.
- Gana quien controle más zonas al final del juego.
- Las posiciones iniciales de los Yoshis son **aleatorias**, no coinciden, y no pueden iniciar dentro de zonas especiales.

---

## 🧠 Inteligencia Artificial

El juego usa un algoritmo **Minimax con decisiones imperfectas** para el Yoshi verde (la IA).

### Niveles de dificultad:

| Nivel        | Profundidad del árbol Minimax |
|--------------|-------------------------------|
| Principiante | 2                             |
| Amateur      | 4                             |
| Experto      | 6                             |

La IA inicia siempre el juego y utiliza una función heurística para evaluar los estados del tablero.

---

## 🛠️ Tecnologías

- Lenguaje: Python 3
- Interfaz gráfica: nextjs
- Algoritmo IA: Minimax con decisiones imperfectas
- Otras dependencias: (agrega aquí si usas alguna librería externa)

---

## ▶️ Instrucciones para ejecutar

1. Clona el repositorio o descomprime el `.rar`:
   ```bash
   git clone https://github.com/tuusuario/yoshis-zones.git
