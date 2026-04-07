from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from dependencies import user_required
from models.asset_model import Asset
from schemas.user_schema import ChangePassword
from utils.hash import verify_password, hash_password
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import user_required, get_db

router = APIRouter(prefix="/user", tags=["User"])

def get_db():
    db = SessionLocal()
    yield db

# View My Assets
@router.get("/my-assets/{user_id}")
def my_assets(user_id: int, db: Session = Depends(get_db)):
    assets = db.query(Asset).filter(Asset.assigned_to == user_id).all()
    return assets

@router.get("/profile")
def get_profile(user=Depends(user_required)):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }

@router.post("/change-password")
def change_password(request: ChangePassword,
                    user=Depends(user_required),
                    db: Session = Depends(get_db)):
     
    old_password = request.old_password.get_secret_value()
    new_password = request.new_password.get_secret_value()

    # Step 1: Check old password
    if not verify_password(old_password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    # Step 2: Update password
    user.password = hash_password(new_password)

    # (Optional but recommended)
    if hasattr(user, "is_first_login"):
        user.is_first_login = 0

    db.commit()

    return {"msg": "Password changed successfully"}