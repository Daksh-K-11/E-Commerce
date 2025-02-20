from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name : str
    phone_number : int
    
class Token(BaseModel):
    access_token : str
    token_type : str
    
class TokenData(BaseModel):
    id : Optional[int] = None