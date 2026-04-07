from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database import SessionLocal
from models.user_model import User
from schemas.user_schema import Login
from schemas.user_schema import UserCreate
from models.user_model import User
from utils.hash import hash_password
from utils.hash import verify_password
from utils.token import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register-admin")
def register_admin(request: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_admin = db.query(User).filter(User.role == "admin").first()
        if existing_admin:
            raise HTTPException(status_code=400, detail="Admin already exists")

        user_exist = db.query(User).filter(User.email == request.email).first()
        if user_exist:
            raise HTTPException(status_code=400, detail="Email already registered")

        new_admin = User(
            name=request.name,
            email=request.email,
            password=hash_password(request.password),
            role="admin"
        )

        db.add(new_admin)
        db.commit()

        return {"msg": "Admin created successfully"}

    except Exception as e:
        print("🔥 ERROR:", str(e))   # 👈 VERY IMPORTANT
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):

    try:
        user = db.query(User).filter(User.email == request.username).first()

        if not user or not verify_password(request.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({
            "user_id": user.id,
            "role": user.role
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except Exception as e:
        print("🔥 LOGIN ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))