"""
Configuration management for the application.
"""
from enum import Enum
from functools import lru_cache
from pydantic_settings import BaseSettings

class Environment(str, Enum):
    """Application environments"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    # Environment
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    
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
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        use_enum_values = True

@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Returns:
        Settings: Application settings
    """
    return Settings()
