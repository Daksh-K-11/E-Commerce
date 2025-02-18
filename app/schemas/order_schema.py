from pydantic import BaseModel
from typing import List
from datetime import datetime
from .product_schema import ProductOut 

class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductOut

    class Config:
        orm_mode = True

class OrderOut(BaseModel):
    id: int
    created_at: datetime
    items: List[OrderItemOut]
    total_amount: float

    class Config:
        orm_mode = True
