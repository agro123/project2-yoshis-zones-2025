from flask import Flask, request, jsonify

app = Flask(__name__)


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

    dificultad = datos.get("dificultad", 1)
    #mejor_mov = obtener_movimiento(estado, dificultad)
    mejor_mov = (0,0)

    return jsonify({"nueva_pos_verde": mejor_mov})

@app.route('/')
def index():
    return "API working!!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
