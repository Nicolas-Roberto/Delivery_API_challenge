from xmlrpc.client import boolean
from pydantic import BaseModel

class Item(BaseModel):
    cliente:str 
    produto:str 
    valor:float 
    