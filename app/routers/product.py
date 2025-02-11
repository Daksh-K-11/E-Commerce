from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Product, ProductImage
from ..schemas.product_schema import ProductCreate, ProductOut, ProductUpdate
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

@router.get("/", response_model=List[ProductOut], status_code=status.HTTP_200_OK)
def get_all_products(db: Session = Depends(get_db)):
    
    products = db.query(Product).all()
    return products

@router.get("/my-products", response_model=List[ProductOut], status_code=status.HTTP_200_OK)
def get_my_products(
    db: Session = Depends(get_db),
    current_user = Depends(seller_required)
):
    
    if not current_user.seller:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not a seller")
    
    products = db.query(Product).filter(Product.seller_id == current_user.seller.id).all()
    return products


@router.patch("/{product_id}", status_code=status.HTTP_202_ACCEPTED, response_model=ProductOut)
def patch_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(seller_required)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    if product.seller_id != current_user.seller.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this product")
    
    if product_update.title is not None:
        product.title = product_update.title
    if product_update.description is not None:
        product.description = product_update.description
    if product_update.price is not None:
        product.price = product_update.price
    if product_update.quantity is not None:
        product.quantity = product_update.quantity
    if product_update.city is not None:
        product.city = product_update.city
    if product_update.extra_specifications is not None:
        product.extra_specifications = product_update.extra_specifications
        
    if product_update.images is not None:
        for image in product.images:
            db.delete(image)
        db.commit()
        
        new_images = []
        for image in product_update.images:
            new_image = ProductImage(
                product_id=product.id,
                image_url=str(image.image_url)
            )
            db.add(new_image)
            new_images.append(new_image)
        product.images = new_images

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user = Depends(seller_required)):
    
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    if current_user.seller.id != product.seller_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this product")
    
    db.delete(product)
    db.commit()
    return None