from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(100), unique=True)
    password = Column(String(255))
    role = Column(String(20))  # admin / user
    is_first_login = Column(Integer, default=1)  # 1 = must change password