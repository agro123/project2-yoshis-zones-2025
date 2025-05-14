from flask import Flask, request, jsonify
from flask_cors import CORS
from minmax import mejor_movimientov1, mejor_movimientov2

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
    mejor_mov = mejor_movimientov2(estado, dificultad)

    return jsonify((mejor_mov))

@app.route('/')
def index():
    return "API working!!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
