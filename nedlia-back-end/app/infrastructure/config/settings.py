"""Application configuration settings."""

from typing import Any, Dict, Optional
from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings

class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    url: PostgresDsn = Field(..., description="PostgreSQL connection URL")
    pool_size: int = Field(default=5, description="Database connection pool size")
    max_overflow: int = Field(default=10, description="Maximum overflow connections")
    pool_timeout: int = Field(default=30, description="Pool timeout in seconds")
    pool_recycle: int = Field(default=1800, description="Connection recycle time")
    echo: bool = Field(default=False, description="Echo SQL queries")

    class Config:
        env_prefix = "DB_"

class RedisSettings(BaseSettings):
    """Redis configuration settings."""
    
    url: RedisDsn = Field(..., description="Redis connection URL")
    pool_size: int = Field(default=10, description="Redis connection pool size")
    pool_timeout: int = Field(default=30, description="Pool timeout in seconds")

    class Config:
        env_prefix = "REDIS_"

class APISettings(BaseSettings):
    """API configuration settings."""
    
    title: str = Field(default="Nedlia Backend API")
    description: str = Field(
        default="Clean Architecture Backend with FastAPI and PostgreSQL"
    )
    version: str = Field(default="0.1.0")
    debug: bool = Field(default=False)
    docs_url: Optional[str] = Field(default="/docs")
    openapi_url: Optional[str] = Field(default="/openapi.json")

    class Config:
        env_prefix = "API_"

class SecuritySettings(BaseSettings):
    """Security configuration settings."""
    
    secret_key: str = Field(..., description="JWT secret key")
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration time in minutes"
    )
    refresh_token_expire_days: int = Field(
        default=7,
        description="Refresh token expiration time in days"
    )
    password_hash_rounds: int = Field(
        default=12,
        description="Number of rounds for password hashing"
    )

    class Config:
        env_prefix = "SECURITY_"

class LoggingSettings(BaseSettings):
    """Logging configuration settings."""
    
    level: str = Field(default="INFO")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    json_logs: bool = Field(default=True)

    class Config:
        env_prefix = "LOG_"

class Settings(BaseSettings):
    """Main application settings."""
    
    environment: str = Field(
        default="development",
        description="Environment (development, staging, production)"
    )
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    api: APISettings = Field(default_factory=APISettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    cors_origins: list[str] = Field(default=["*"])
    metrics_enabled: bool = Field(default=True)
    tracing_enabled: bool = Field(default=True)

    def get_database_settings(self) -> Dict[str, Any]:
        """Get SQLAlchemy database settings."""
        return {
            "pool_size": self.database.pool_size,
            "max_overflow": self.database.max_overflow,
            "pool_timeout": self.database.pool_timeout,
            "pool_recycle": self.database.pool_recycle,
            "echo": self.database.echo,
        }

    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
