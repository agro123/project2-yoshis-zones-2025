def heuristica(estado):
    return (
        (estado["zonas_verde"] - estado["zonas_rojo"]) * 10 +
        (len(estado["casillas_verde"]) - len(estado["casillas_rojo"]))
    )
