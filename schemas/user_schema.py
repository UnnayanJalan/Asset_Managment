from pydantic import BaseModel, EmailStr, SecretStr, Field

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., max_length=200)

class Login(BaseModel):
    email: str
    password: str

class ChangePassword(BaseModel):
    old_password: SecretStr
    new_password: SecretStr