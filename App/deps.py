from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .auth import get_current_user
from . import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_active_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
