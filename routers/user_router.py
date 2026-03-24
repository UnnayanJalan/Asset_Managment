from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.asset_model import Asset

router = APIRouter(prefix="/user", tags=["User"])

def get_db():
    db = SessionLocal()
    yield db

# View My Assets
@router.get("/my-assets/{user_id}")
def my_assets(user_id: int, db: Session = Depends(get_db)):
    assets = db.query(Asset).filter(Asset.assigned_to == user_id).all()
    return assets