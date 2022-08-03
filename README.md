# Delivery_API_challenge

Essa é uma API chamada de "delivery-api" foi desenvolvida para o desafio do cblab, ela permite realizar o CRUD de um pedido além de permitir alterar seu estado.

## 🚀 Começando

Clone o repositório.
```
$ git clone https://github.com/Nicolas-Roberto/Delivery_API_challenge.git
```

Rode o docker
```
$ docker build -t myimage .

$ docker run -d --name  mycontainer -p 80:80 myimage
```

Vá para a pasta app
```
$ cd app
```

Rode a main
```
$ uvicorn main:app 
```

Abra no navegador 
```
http://127.0.0.1:8000/docs#/
```

## 🛠️ Construído com

* [FastAPI](https://fastapi.tiangolo.com/) 
* [pydantic](https://pydantic-docs.helpmanual.io/) 
* [Uvicorn](https://www.uvicorn.org/) 


## 📦 Desenvolvimento

Os dados são armazenados em memória durante a execução
da API, o funcionamento do sistema pode ser visto neste diagrama:

*Diagrama da API*
<img align="center" 
       src="docs/diagrams/API-diagrama.png"/>

<br/>
Além do CRUD, a máquina de estados foi implementada seguindo o seguinte diagrama.

*Diagrama de estados*
<img align="center" 
       src="docs/diagrams/state-diagram.png"/>

       
