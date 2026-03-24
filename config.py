# from pydantic import BaseSettings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://root:1234@localhost/asset_db"
    
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

settings = Settings()