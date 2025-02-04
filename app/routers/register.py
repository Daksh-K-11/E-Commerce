from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from ..schemas.user_schema import UserCreate, UserOut


router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
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

