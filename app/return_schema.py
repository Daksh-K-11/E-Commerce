from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReturnOrderOut(BaseModel):
    id: int
    order_id: int
    user_id: int
    reason: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
