from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from ..schemas.user_schema import UserCreate, UserOut
from ..schemas.seller_schema import SellerCreate, SellerOut


router = APIRouter(tags=["Users"])

@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    if db.query(models.User).filter(models.User.phone_number == user.phone_number).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered",
        )

    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/seller", status_code=status.HTTP_201_CREATED, response_model=SellerOut)
def create_seller(seller: SellerCreate, db : Session = Depends(get_db)):
    
    if db.query(models.User).filter(models.User.email == seller.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    if db.query(models.User).filter(models.User.phone_number == seller.phone_number).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered",
        )

    hashed_password = utils.hash(seller.password)
    seller.password = hashed_password
    new_user = models.User(
        name=seller.name,
        phone_number=seller.phone_number,
        email=seller.email,
        address=seller.address,
        password=hashed_password,
        role="seller" 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_seller = models.Seller(
        id=new_user.id,
        store_name=seller.store_name,
        business_license=seller.business_license,
        tax_id=seller.tax_id
    )
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)

    seller_data = {
        "id": new_user.id,
        "name": new_user.name,
        "phone_number": new_user.phone_number,
        "email": new_user.email,
        "address": new_user.address,
        "created_at": new_user.created_at,
        "role": new_user.role,
        "store_name": new_seller.store_name,
        "business_license": new_seller.business_license,
        "tax_id": new_seller.tax_id,
    }
    return seller_data