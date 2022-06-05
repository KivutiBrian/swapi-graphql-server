import secrets
from typing import List, Optional
from pydantic import BaseSettings, AnyHttpUrl

class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = 120
    ALGORITHM: str

    # read from .env file
    class Config:
        env_file = ".env"

settings = Settings()
