from flask import Flask, request, jsonify
from flask_cors import CORS
from minmax import obtener_mejor_movimiento

"""
Juego de Caballos en Tablero 8x8

Dos jugadores que son yoshi's se mueven como caballos de ajedrez con el objetivo de conquistar la mayor cantidad de casillas especiales.
Cada jugador comienza de manera aleatoria en el tablero. En cada turno, el jugador puede moverse a una casilla válida según el patrón
de movimiento del caballo. Las casillas especiales por las que pasa un jugador se "pintan" de su color.  
Estas casillas ya no son accesibles para el jugador de otros color.

Estructura del código:
- helpers: Calculo del estado del juego (tablero, posiciones, zonas)
- Heurística: Evaluación de estados
- Minimax: Búsqueda del mejor movimiento para el jugador actual (maquina)
"""

app = Flask(__name__)
CORS(app)

@app.route('/play', methods=['POST'])
def jugar():
    datos = request.get_json()
    estado = {
        "pos_verde": tuple(datos["pos_verde"]),
        "pos_rojo": tuple(datos["pos_rojo"]),
        "casillas_verde": set(map(tuple, datos["casillas_verde"])),
        "casillas_rojo": set(map(tuple, datos["casillas_rojo"])),
        "zonas_verde": datos["zonas_verde"],
        "zonas_rojo": datos["zonas_rojo"]
    }
    dificultad = datos["dificultad"]
    print('dificultad', dificultad)
    mejor_mov = obtener_mejor_movimiento(estado, dificultad)

    ya_pintadas = estado["casillas_verde"] | estado["casillas_rojo"]
    if mejor_mov in ya_pintadas:
        print("⚠️ ERROR: El movimiento sugerido ya está pintado:", mejor_mov)
        return jsonify({"error": "Movimiento inválido: ya pintado"}), 400

    return jsonify((mejor_mov))

@app.route('/')
def index():
    return "API working!!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=32001)
