from pydantic import BaseModel
from typing import List
from .product_schema import ProductOut 

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductOut

    class Config:
        orm_mode = True


class CartOut(BaseModel):
    id: int
    items: List[CartItemOut]
    total_amount: float

    class Config:
        orm_mode = True

