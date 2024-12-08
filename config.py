"""
Configuration management for the application.
Uses environment variables for sensitive data.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # GrowthBook settings
    GROWTHBOOK_API_HOST: str = "https://cdn.growthbook.io"
    GROWTHBOOK_CLIENT_KEY: str
    
    # Environment name
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Returns:
        Settings: Application settings
    """
    return Settings()
