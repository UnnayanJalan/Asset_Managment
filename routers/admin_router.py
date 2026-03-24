from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user_model import User
from models.asset_model import Asset
from utils.hash import hash_password
from schemas.asset_schema import AssetCreate
from dependencies import admin_required
from dependencies import user_required

router = APIRouter(prefix="/admin", tags=["Admin"])

def get_db():
    db = SessionLocal()
    yield db

# Create User
@router.post("/create-user")
def create_user(name: str, email: str, password: str,
                db: Session = Depends(get_db),
                admin=Depends(admin_required)):

    user = User(
        name=name,
        email=email,
        password=hash_password(password),  # 🔥 FIX
        role="user"
    )

    db.add(user)
    db.commit()

    return {"msg": "User created"}

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
def assign_asset(asset_id: int, user_id: int, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    asset.assigned_to = user_id
    db.commit()
    return {"msg": "Asset assigned"}

@router.get("/my-assets")
def my_assets(user=Depends(user_required),
              db: Session = Depends(get_db)):

    return db.query(Asset).filter(Asset.assigned_to == user.id).all()