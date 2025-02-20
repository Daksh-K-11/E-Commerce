from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..database import get_db
from ..models import Order, ReturnOrder
from ..dependencies import get_current_user
from ..config import settings
from ..schemas.return_schema import ReturnOrderOut
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/return", tags=["Return"])

class ReturnRequest(BaseModel):
    order_id: int
    reason: Optional[str] = None

@router.post("/", response_model=ReturnOrderOut, status_code=status.HTTP_200_OK)
def return_order(return_req: ReturnRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    order = db.query(Order).filter(Order.id == return_req.order_id, Order.user_id == current_user.id).first()
    if not order:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    allowed_return_days = settings.return_days
    if datetime.utcnow() > order.created_at + timedelta(days=allowed_return_days):
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Return period has expired")
    
    return_order_record = ReturnOrder(order_id=order.id, user_id=current_user.id, reason=return_req.reason)
    db.add(return_order_record)
    db.commit()
    db.refresh(return_order_record)
    
    return return_order_record
