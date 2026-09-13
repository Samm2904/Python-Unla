from pydantic import BaseModel, Field
from datetime import date, time

class ProductCreate(BaseModel):
    name: str
    price: float

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes=True

class SaleCreate(BaseModel):
   # date: date
    # time: time no se pide porque sino lo tengo q poner a mano
    quantity: int
    product_id: int

    class Config:
        from_attributes = True

class SaleResponse(BaseModel):
    id: int
    date: date 
    time: time 
    quantity: int
    product: ProductResponse
    total_price: float

    class Config:
        from_attributes = True


#Preguntar si se puede hacer un schema para cambiar solamente el precio en vez de todo el producto
