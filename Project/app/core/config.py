from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    env: str = "development"
    debug: bool = False
    database_url: str

    model_config = SettingsConfigDict(env_file=f"envs/.env.{env}", env_file_encoding="utf-8")

settings = Settings()
