import random
import string
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.user_model import User
from models.asset_model import Asset
from schemas.user_schema import UserCreate
from schemas.asset_schema import AssetCreate
from dependencies import admin_required, user_required
from utils.hash import hash_password
from utils.email import send_email

router = APIRouter(prefix="/admin", tags=["Admin"])


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create User
@router.post("/create-user")
async def create_user(request: UserCreate,
                      db: Session = Depends(get_db),
                      admin=Depends(admin_required)):

    # check if user exists
    user_exist = db.query(User).filter(User.email == request.email).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="User already exists")

    # generate password
    default_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    # create user
    new_user = User(
        name=request.name,
        email=request.email,
        password=hash_password(default_password),
        role="user",
        is_first_login=1
    )

    db.add(new_user)
    db.commit()

    # 🔥 send email
    send_email(request.email, default_password)

    return {"msg": "User created and email sent"}


# Add Asset
@router.post("/add-asset")
def add_asset(asset: AssetCreate,
              db: Session = Depends(get_db),
              admin=Depends(admin_required)):

    new_asset = Asset(name=asset.name, type=asset.type)
    db.add(new_asset)
    db.commit()

    return {"msg": "Asset added"}


# Assign Asset
@router.post("/assign-asset")
def assign_asset(asset_id: int,
                 user_id: int,
                 db: Session = Depends(get_db),
                 admin=Depends(admin_required)):

    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    asset.assigned_to = user_id
    db.commit()

    return {"msg": "Asset assigned"}


# Ideally move this to user_router.py
@router.get("/my-assets")
def my_assets(user=Depends(user_required),
              db: Session = Depends(get_db)):

    assets = db.query(Asset).filter(Asset.assigned_to == user.id).all()
    return assets