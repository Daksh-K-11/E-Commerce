from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from ..schemas.customer_schema import CustomerCreate, CustomerOut


router = APIRouter(prefix="/customer", tags=["Customers"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CustomerOut)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    
    if db.query(models.Customer).filter(models.Customer.email == customer.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    if db.query(models.Customer).filter(models.Customer.phone_number == customer.phone_number).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered",
        )

    
    hashed_password = utils.hash(customer.password)
    customer.password = hashed_password

    
    new_customer = models.Customer(**customer.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer

