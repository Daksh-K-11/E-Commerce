from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Product, Cart, CartItem
from ..schemas.cart_schema import CartItemCreate, CartOut
from ..dependencies import get_current_user

router = APIRouter(tags=["Cart"])

@router.patch("/cart", response_model=CartOut, status_code=status.HTTP_200_OK)
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
    
    # Retrieve the user's cart, or create one if it doesn't exist.
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    # Check if the product is already in the cart.
    cart_item = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart.id, CartItem.product_id == item.product_id)
        .first()
    )
    if cart_item:
        # Calculate new quantity and validate it.
        new_quantity = cart_item.quantity + item.quantity
        if new_quantity > product.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Total quantity in cart exceeds available stock"
            )
        cart_item.quantity = new_quantity
    else:
        # Create a new cart item.
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart)
    return cart


