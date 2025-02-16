"""
Application configuration
"""

from functools import lru_cache
from typing import Optional

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Nedlia Backend"
    DEBUG: bool = False
    VERSION: str = "1.0.0"

    # GrowthBook
    GROWTHBOOK_API_HOST: str = "https://cdn.growthbook.io"
    GROWTHBOOK_CLIENT_KEY: str = "test_key"  # Default test key
    GROWTHBOOK_CACHE_TTL: int = 60  # Cache features for 60 seconds

    # Database - using test defaults
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "test_user"
    DB_PASSWORD: str = "test_password"
    DB_NAME: str = "test_db"

    # Optional environment indicator
    ENV: Optional[str] = Field(default="test")

    model_config = ConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Allow extra fields
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings"""
    return Settings()
