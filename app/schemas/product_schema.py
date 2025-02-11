from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

class ProductImage(BaseModel):
    image_url: HttpUrl
    
class ProductCreate(BaseModel):
    title: str
    description:str
    price: Decimal
    quantity: int
    city: str
    extra_specifications: Optional[dict] = None
    images: List[ProductImage] = Field(..., min_items=1, max_items=5)
    
    
class ProductUpdate(BaseModel):
    title: Optional[str]
    descritpion: Optional[str]
    price: Optional[Decimal]
    quantity: Optional[int]
    city: Optional[str]
    extra_specifications: Optional[dict] = None
    images: Optional[List[ProductImage]] = Field(
        None, 
        min_items=1, 
        max_items=5, 
        description="If provided, replaces all existing images."
    )
    
    
class ProductOut(BaseModel):
    id: int
    title: str
    description: str
    price: Decimal
    quantity: int
    city: str
    extra_specifications: Optional[dict] = None
    images: List[ProductImage]

    class Config:
        orm_mode = True