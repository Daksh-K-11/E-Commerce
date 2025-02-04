from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class CustomerCreate(BaseModel):
    name: str
    phone_number: int
    email: EmailStr
    address: Optional[str] = None
    password: str


class CustomerOut(BaseModel):
    id: int
    name: str
    phone_number: int
    email: EmailStr
    address: Optional[str]
    created_at: datetime
    role: str
    
    class Config:
        from_attributes = True
