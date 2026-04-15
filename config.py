# from pydantic import BaseSettings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MAIL_USERNAME: str = "unnayan.jalan@acldigital.com"
    MAIL_PASSWORD: str = "gtjyjbbefkavbgjf"
    MAIL_FROM: str = "unnayan.jalan@acldigital.com"

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