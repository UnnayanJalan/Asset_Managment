from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from database import SessionLocal
from models.user_model import User
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get Current User from Token
def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("user_id")

        user = db.query(User).filter(User.id == user_id).first()

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # if not user:
        #     raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Token error")


# Admin Only Access
def admin_required(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user


# User Access
def user_required(user: User = Depends(get_current_user)):
    return user