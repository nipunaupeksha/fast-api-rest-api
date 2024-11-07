import os
from pydantic_settings import BaseSettings, SettingsConfigDict


# Get the settings from the .env file
class Settings(BaseSettings):
    API_STR: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_POOL_SIZE: int
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    ADMIN_USERNAME: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../../.env"),
        env_file_encoding="utf-8",
    )


settings = Settings()
