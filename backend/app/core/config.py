from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        env_prefix="",
        extra="ignore",
    )

    database_url: str
    secret_key: str = Field(min_length=32)

settings = Settings()