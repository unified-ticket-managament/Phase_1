# config.py

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    app_name: str = "Ticket Management System"
    app_env: str = "development"
    debug: bool = False

    api_v1_prefix: str = "/api/v1"

    database_url: str

    log_level: str = "INFO"


@lru_cache
def get_settings():
    return Settings()