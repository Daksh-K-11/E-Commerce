from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models import ProductRating, Order, OrderItem
from ..schemas.rating_schema import RatingOut, RatingCreate
from ..dependencies import get_current_user
from ..database import get_db

router = APIRouter(prefix="/rating", tags=["Rating"])

@router.post("/", response_model=RatingOut, status_code=status.HTTP_200_OK)
def rate_product(rating_data: RatingCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    order_item = (
        db.query(OrderItem)
          .join(Order)
          .filter(Order.user_id == current_user.id, OrderItem.product_id == rating_data.product_id)
          .first()
    )
    if not order_item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot rate a product you haven't purchased")
    
    existing_rating = db.query(ProductRating).filter(
        ProductRating.product_id == rating_data.product_id,
        ProductRating.user_id == current_user.id
    ).first()
    
    if existing_rating:
        existing_rating.rating = rating_data.rating
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
    else:
        new_rating = ProductRating(product_id=rating_data.product_id, user_id=current_user.id, rating=rating_data.rating)
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        return new_rating
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(id: int ,db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    
    rating = db.query(ProductRating).filter(ProductRating.id==id, ProductRating.user_id==current_user.id).first()
    
    if not rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such product")
    
    db.delete(rating)
    db.commit()
    return None