from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    bot_token: str
    redis_url: str = "redis://localhost:6379/0"
    api_base_url: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

config: Settings = Settings()
