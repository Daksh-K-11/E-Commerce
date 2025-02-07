from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import oauth2, models
from .database import get_db

def get_current_user(token: str = Depends(oauth2.oauth2_scheme), db: Session=Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token = oauth2.verify_access_token(token, credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user

def seller_required(current_user: models.User = Depends(get_current_user)):
    
    if current_user.role != "seller":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a seller"
        )
    
    return current_user