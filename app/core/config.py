"""
Application configuration
"""

from functools import lru_cache

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_V1_STR: str
    PROJECT_NAME: str
    DEBUG: bool
    VERSION: str = "1.0.0"

    # GrowthBook
    GROWTHBOOK_API_HOST: str
    GROWTHBOOK_CLIENT_KEY: str  # Set this in your environment
    GROWTHBOOK_CACHE_TTL: int  # Cache features for 60 seconds

    # Database
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    model_config = ConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings"""
    return Settings()
