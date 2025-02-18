from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Cart
from ..dependencies import get_current_user
from ..config import settings

import qrcode
from io import BytesIO
from fastapi.responses import JSONResponse
import base64

router = APIRouter(tags=["Payment"], prefix="/payment")

@router.get("/", status_code=status.HTTP_200_OK)
def generate_gpay_qr_code(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart or not cart.items:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart is empty")
    
    total_amount = cart.total_amount

    upi_id = settings.upi_id
    merchant_name = "Daksh Khinvasara"
    transaction_note = "Payment for E-Commerce"

    upi_uri = (
        f"upi://pay?"
        f"pa={upi_id}&"
        f"pn={merchant_name}&"
        f"am={total_amount:.2f}&"
        f"cu=INR&"
        f"tn={transaction_note}"
    )
    
    qr = qrcode.QRCode(
         version=1,
         error_correction=qrcode.constants.ERROR_CORRECT_L,
         box_size=10,
         border=4,
    )
    qr.add_data(upi_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    
    encoded_img = base64.b64encode(buf.getvalue()).decode('utf-8')
    data_url = f"data:image/png;base64,{encoded_img}"
    
    return {"qr_code_url": data_url}
