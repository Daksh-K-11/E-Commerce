# from fastapi import HTTPException, APIRouter, Depends, status
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from app.schemas.auth_schema import Customer

# from .. import database, utils, oauth2, models

# router = APIRouter(tags=['Authentication'])

# @router.post("/login", response_model = Customer)
# def login(user_credentials : OAuth2PasswordRequestForm=Depends(), db: Session=Depends(database.get_db)):
    
#     customer = db.query(models.Customer).filter(models.Customer.phone_number == user_credentials.username).first()
    
#     if customer is None:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
#     if not utils.verify(user_credentials.password, customer.password):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
#     access_token = oauth2.create_access_token(data={"id": customer.id})
    
#     return {"acces_token": access_token, "token_type": "Bearer"}



from fastapi import HTTPException, APIRouter, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, utils, oauth2, models
from ..schemas.auth_schema import Token

router = APIRouter(tags=['Authentication'])

# @router.post("/login", response_model=Token)
# def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
#     print("entered login")
    
#     customer = db.query(models.Customer).filter(models.Customer.email == user_credentials.username).first()
    
#     print("after customer")

#     if not customer:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, 
#             detail="Invalid Credentials"
#         )
        
#     print("after first if")
    
#     if not utils.verify(user_credentials.password, customer.password):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, 
#             detail="Invalid Credentials"
#         )
    
#     print("after first if")

#     access_token = oauth2.create_access_token(data={"id": customer.id})
    
#     print("before return")

#     return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    print(f"Username: {user_credentials.username}")
    print(f"Password: {user_credentials.password}")
    
    customer = db.query(models.Customer).filter(models.Customer.email == user_credentials.username).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid Credentials"
        )
    
    if not utils.verify(user_credentials.password, customer.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid Credentials"
        )

    access_token = oauth2.create_access_token(data={"id": customer.id})

    return {"access_token": access_token, "token_type": "Bearer"}
