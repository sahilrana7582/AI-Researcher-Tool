from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    environment: Literal["dev", "prod"]
    llm_api_key: SecretStr

    model_config = SettingsConfigDict(
        env_file="/Users/apple/Desktop/projects/genai/AI Researcher/.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()