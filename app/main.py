from fastapi import FastAPI, Query, Request
import schemas
import json
import datetime 

#valid state order, 1 to invalid and 0 to valid
def validation(state:str, newState:str):
    valid=False
    if(state!="DELIVERED" and state!="CANCELED" and newState=="CANCELED"): valid=True
    if(state=="RECEIVED" and newState=="CONFIRMED"): valid=True
    if(state=="CONFIRMED" and newState=="DISPATCHED"): valid=True
    if(state=="DISPATCHED" and newState=="DELIVERED"): valid=True

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
    return "ID inválido!"

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
                        "timestamp": datetime.datetime.today()}
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
            if pedidos["pedidos"][i]["estado"] == "RECEIVED" or pedidos["pedidos"][i]["estado"] == "CONFIRMED":
                pedidos["pedidos"][i] = {
                            "id": id_order,
                            "cliente": order.cliente,
                            "produto": order.produto,
                            "valor": order.valor,
                            "entregue": False,
                            "estado": "RECEIVED",
                            "timestamp": datetime.datetime.today()}
                return pedidos["pedidos"][i]
    return "ID inválido!"

#end point to change state order
@app.put("/states/{id_order}")
def update_state_order(id_order:int, choice: str = Query("RECEIVED", enum=("RECEIVED","CONFIRMED","DISPATCHED","CANCELED","DELIVERED"))):
    size = len(pedidos["pedidos"])  
    for i in range(size):
        if pedidos["pedidos"][i] is None: continue
        if pedidos["pedidos"][i]["id"] == id_order:
            if(validation(pedidos["pedidos"][i]["estado"], choice)):
                pedidos["pedidos"][i]["estado"] = choice
                pedidos["pedidos"][i]["timestamp"] = datetime.datetime.today()
                
                if choice == "DELIVERED":
                    pedidos["pedidos"][i]["entregue"]=True
                
                return pedidos["pedidos"][i]

    return "Estado ou ID inválido!"

#end point to delete order
@app.delete("/delete/{id_order}")
def delete_order(id_order:int):
    size = len(pedidos["pedidos"])
    for i in range(size):
        if pedidos["pedidos"][i] is None: continue
        if pedidos["pedidos"][i]["id"] == id_order:
            del pedidos["pedidos"][i]
            return "Pedido " + id_order + "deletado."
    return "ID inválido!"