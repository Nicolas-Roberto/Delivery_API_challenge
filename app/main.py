from curses.panel import new_panel
from enum import Enum
from os import times
from pipes import Template
from random import choices
from typing import Union
from xmlrpc.client import boolean

from fastapi import FastAPI, Query, Request
import schemas
import json

#valid state order, 1 to invalid and 0 to valid
def validation(state:str, newState:str):
    valid=1
    if(state!="DELIVERED" and state!="CANCELED" and newState=="CANCELED"): valid=0
    if(state=="RECEIVED" and newState=="CONFIRMED"): valid=0
    if(state=="CONFIRMED" and newState=="DISPATCHED"): valid=0
    if(state=="DISPATCHED" and newState=="DELIVERED"): valid=0

    return valid


# open and save pedidos.json in padidos
with open("pedidos.json", encoding='utf-8') as pedidos_json:
    pedidos = json.load(pedidos_json)

#run app
app = FastAPI()


#home page, order list
@app.get("/")
def read_root():
    return pedidos["pedidos"]

#end point to view specific order
@app.get("/items/{id_order}")
def read_item(id_order:int):
    #getId(id_order)
    size = len(pedidos["pedidos"])
    for item in pedidos["pedidos"]:
        if item is None: continue
        if item["id"] == id_order:
            return item
    return 

#end point to create order
@app.post("/create")
def create_order(order:schemas.Item):
    newId = pedidos["nextId"]
    new_pedido = dict()
    new_pedido = {"id": newId,
                        "cliente": order.cliente,
                        "produto": order.produto,
                        "valor": order.valor,
                        "entregue": False,
                        "estado": "RECEIVED",
                        "timestamp": order.timestamp}
    pedidos["pedidos"].append(new_pedido)
    pedidos["nextId"] = newId+1
    
    return pedidos["pedidos"][len(pedidos["pedidos"])-1]


#end point to update a order
@app.put("/update/{id_order}")
def update_order(id_order:int, order:schemas.Item):
    size = len(pedidos["pedidos"])  
    for i in range(size):
        if pedidos["pedidos"][i] is None: continue
        if pedidos["pedidos"][i]["id"] == id_order:
            pedidos["pedidos"][i] = {
                        "id": id_order,
                        "cliente": order.cliente,
                        "produto": order.produto,
                        "valor": order.valor,
                        "entregue": order.entrege,
                        "estado": order.estado,
                        "timestamp": order.timestamp}
            return pedidos["pedidos"][i]
    return 

#end point to change state order
@app.put("/states/{id_order}")
def update_order(id_order:int, choice: str = Query("RECEIVED", enum=("RECEIVED","CONFIRMED","DISPATCHED","CANCELED","DELIVERED"))):
    size = len(pedidos["pedidos"])  
    for i in range(size):
        if pedidos["pedidos"][i] is None: continue
        if pedidos["pedidos"][i]["id"] == id_order:
            if(validation(pedidos["pedidos"][i]["estado"], choice)==0):
                pedidos["pedidos"][i]["estado"] = choice
                return pedidos["pedidos"][i]

    return "Estado inválido!"

#end point to delete order
@app.delete("/delete/{id_order}")
def delete_order(id_order:int):
    size = len(pedidos["pedidos"])
    for i in range(size):
        if pedidos["pedidos"][i] is None: continue
        if pedidos["pedidos"][i]["id"] == id_order:
            del pedidos["pedidos"][i]
            return pedidos
    return pedidos