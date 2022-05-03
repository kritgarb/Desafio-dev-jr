from typing import Optional
import uvicorn
from fastapi import FastAPI, Body
from app.examples import *
from app.models.rota import Rota

app = FastAPI()
listaRotas = []


# Salvar Grafo
@app.post("/graph")
async def salvar_grafo(rota: Rota = Body(example_graph)):
    rota.id = (len(listaRotas) + 1)
    listaRotas.append(rota)
    return rota


# Recuperar Grafo
@app.get("/graph/{graphId}")
async def recuperar_grafo(graphId: int):
    for grafo in listaRotas:
        if grafo.id == graphId:
            return grafo
    return {"Status": 404, "Mensagens": "Grafo não encontrado"}


def procurar(town1, town2, rota, listaEncontrada):
    if len(town1) != len(set(town1)): return

    if town1[-1] == town2:
        listaEncontrada.append(town1)
        return
    else:
        novas_rotas = []
        for aresta in rota.data:
            if aresta.source.lower() == town1[-1].lower():
                novas_rotas.append(aresta.target.lower())

    for i in novas_rotas:
        novoOrigem = town1.copy()
        novoOrigem.append(i.lower())
        procurar(novoOrigem, town2, rota, listaEncontrada)


# Buscar melhor rota
@app.post("/routes/{graphId}/from/{town1}/to/{town2}/")
async def buscar_rota(graphId: int, town1: str, town2: str, maxStops: Optional[int] = None):
    listaEncontrada = []
    listaSerializada = []

    for rota in listaRotas:
        if rota.id == graphId:
            procurar([town1], town2, rota, listaEncontrada)

    for i in listaEncontrada:
        if maxStops is None or (len(i) - 1) <= maxStops:
            listaSerializada.append({"route": ''.join(i).upper(), "stops": (len(i) - 1)})

    return {"routes": listaSerializada}


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
