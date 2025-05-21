from flask import Flask, request, jsonify
from flask_cors import CORS
from minmax import obtener_mejor_movimiento

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
    app.run(debug=True, host='0.0.0.0', port=5000)
