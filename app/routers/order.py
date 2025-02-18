from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Product, Cart, CartItem, Order, OrderItem
from ..schemas.order_schema import OrderOut
from ..dependencies import get_current_user

router = APIRouter(tags=["Order"], prefix="/order")

@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def place_order(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty")
    
    for cart_item in cart.items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {cart_item.product_id} not found"
            )
        if product.quantity < cart_item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product '{product.title}'"
            )
    
    order = Order(user_id=current_user.id)
    db.add(order)
    db.commit()
    db.refresh(order)
    
    for cart_item in cart.items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        product.quantity -= cart_item.quantity
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity
        )
        db.add(order_item)
    
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    
    db.commit()
    db.refresh(order)
    return order
