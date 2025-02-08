"""
Core configuration for the application.
"""

from enum import Enum
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Application environments"""

    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "Nedlia API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Environment
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # Feature Flags
    GROWTHBOOK_API_HOST: str = "https://cdn.growthbook.io"
    GROWTHBOOK_CLIENT_KEY: str
    GROWTHBOOK_CACHE_TTL: int = 60

    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.ENVIRONMENT == Environment.DEVELOPMENT

    @property
    def is_testing(self) -> bool:
        """Check if running in testing environment"""
        return self.ENVIRONMENT == Environment.TESTING

    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT == Environment.PRODUCTION

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, use_enum_values=True
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Returns:
        Settings: Application settings
    """
    return Settings()
