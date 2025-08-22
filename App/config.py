import os
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    
    # Optional Environment Variables (không bắt buộc)
    ENV: str = "development"
    DEBUG: str = "True"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",  # Thay đổi từ "forbid" thành "ignore"
    }
    
    def __init__(self, **kwargs):
        # Tìm file .env ở thư mục gốc của dự án
        project_root = Path(__file__).parent.parent
        env_file = project_root / ".env"
        
        if env_file.exists():
            self.model_config["env_file"] = str(env_file)
        
        super().__init__(**kwargs)
    
    @property
    def is_development(self) -> bool:
        return self.ENV.lower() == "development"
    
    @property
    def is_debug(self) -> bool:
        return self.DEBUG.lower() in ("true", "1", "yes")

settings = Settings()
