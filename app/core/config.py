import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    DEFAULT_USER_USERNAME: str = os.getenv("DEFAULT_USER_USERNAME", "admin")
    DEFAULT_USER_EMAIL: str = os.getenv("DEFAULT_USER_EMAIL", "admin@example.com")
    DEFAULT_USER_PASSWORD: str = os.getenv("DEFAULT_USER_PASSWORD", "admin123")

    class Config:
        env_file = ".env"

settings = Settings()
