import os
from pydantic_settings import BaseSettings, SettingsConfigDict


# Get the settings from the .env file
class Settings(BaseSettings):
    API_STR: str = "/api/v1"
    SECRET_KEY: str = "nipunaupeksha"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 38
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_HOST: str = "35.226.87.163"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "adastra_db"
    DATABASE_POOL_SIZE: int = 100
    ADMIN_EMAIL: str = "admin@email.com"
    ADMIN_PASSWORD: str = "admin123"
    ADMIN_USERNAME: str = "admin"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../../.env"),
        env_file_encoding="utf-8",
    )


settings = Settings()
