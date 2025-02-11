from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Product, ProductImage
from ..schemas.product_schema import ProductCreate, ProductOut
from ..dependencies import seller_required
from typing import List

router = APIRouter(prefix="/product", tags=["Products"])

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(seller_required)
):
    if not current_user.seller:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not a seller")
    
    new_product = Product(
        seller_id = current_user.seller.id,
        title = product.title,
        description = product.description,
        price = product.price,
        quantity = product.quantity,
        city = product.city,
        extra_specifications = product.extra_specifications,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    for image in product.images:
        new_image = ProductImage(
        product_id=new_product.id,
        image_url=str(image.image_url)
        )
        db.add(new_image)

    db.commit()
    db.refresh(new_product)

    return new_product

@router.get("/", response_model=List[ProductOut])
def get_all_products(db: Session = Depends(get_db)):
    
    products = db.query(Product).all()
    return products
