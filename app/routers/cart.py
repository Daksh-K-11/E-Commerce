from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Product, Cart, CartItem
from ..schemas.cart_schema import CartItemCreate, CartOut
from ..dependencies import get_current_user

router = APIRouter(prefix="/cart",tags=["Cart"])

@router.get("/", response_model=CartOut, status_code=status.HTTP_200_OK)
def get_cart(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    
    return cart

@router.patch("/", response_model=CartOut, status_code=status.HTTP_200_OK)
def add_item_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Add an item to the user's cart (or update its quantity) ensuring the quantity does not exceed the available stock.
    """
    
    
    
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    if item.quantity > product.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Requested quantity exceeds available stock"
        )
    
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    cart_item = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart.id, CartItem.product_id == item.product_id)
        .first()
    )
    if cart_item:
        new_quantity = cart_item.quantity + item.quantity
        if new_quantity > product.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Total quantity in cart exceeds available stock"
            )
        cart_item.quantity = new_quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart)
    return cart


