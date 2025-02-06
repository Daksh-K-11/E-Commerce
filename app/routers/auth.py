from fastapi import HTTPException, APIRouter, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, utils, oauth2, models
from ..schemas.auth_schema import Token

router = APIRouter(tags=['Authentication'])


@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    print(f"Username: {user_credentials.username}")
    print(f"Password: {user_credentials.password}")
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid Credentials"
        )
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid Credentials"
        )

    access_token = oauth2.create_access_token(data={"id": user.id, "role": user.role})

    return {"access_token": access_token, "token_type": "Bearer"}
