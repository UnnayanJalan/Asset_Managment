from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., max_length=200)

class Login(BaseModel):
    email: str
    password: str