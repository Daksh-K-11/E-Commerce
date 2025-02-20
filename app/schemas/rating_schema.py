from pydantic import BaseModel
from typing import Literal

class RatingCreate(BaseModel):
    product_id: int
    rating: Literal[1,2,3,4,5]

class RatingOut(BaseModel):
    product_id: int
    user_id: int
    rating: int

    class Config:
        orm_mode = True
