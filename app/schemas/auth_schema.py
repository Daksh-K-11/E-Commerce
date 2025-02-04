from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal

class User(BaseModel):
    name : str
    phone_number : int
    
class Token(BaseModel):
    access_token : str
    token_type : str
    
class TokenData(BaseModel):
    id : Optional[int] = None