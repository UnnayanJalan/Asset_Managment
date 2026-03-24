from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    type = Column(String(50))
    assigned_to = Column(Integer, ForeignKey("users.id"))