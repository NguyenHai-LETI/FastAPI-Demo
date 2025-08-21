import os

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = {
        "env_file": ".env",
        "extra": "forbid",  # bỏ extra fields
    }

settings = Settings()
