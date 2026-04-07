# from pydantic import BaseSettings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MAIL_USERNAME: str = "your_email@yopmail.com"
    MAIL_PASSWORD: str = "your_app_password"
    MAIL_FROM: str = "your_email@yopmail.com"

    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

    DATABASE_URL: str = "mysql+pymysql://root:1234@localhost/asset_db"
    
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    class Config:
        env_file = ".env"   # 🔥 IMPORTANT

settings = Settings()