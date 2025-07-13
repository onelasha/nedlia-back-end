"""Application configuration settings."""

from typing import Any, Dict, List
from pydantic import Field, RedisDsn, HttpUrl, SecretStr
from pydantic_settings import BaseSettings

class DatabaseSettings(BaseSettings):
    """MongoDB configuration settings."""
    url: str = Field(..., env='DB_URL')
    name: str = Field(..., env='DB_NAME')
    min_pool_size: int = Field(5, env='DB_MIN_POOL_SIZE')
    max_pool_size: int = Field(10, env='DB_MAX_POOL_SIZE')
    max_idle_time_ms: int = Field(30000, env='DB_MAX_IDLE_TIME_MS')
    connect_timeout_ms: int = Field(20000, env='DB_CONNECT_TIMEOUT_MS')
    server_selection_timeout_ms: int = Field(30000, env='DB_SERVER_SELECTION_TIMEOUT_MS')

    class Config:
        env_prefix = "DB_"

class RedisSettings(BaseSettings):
    """Redis configuration settings."""
    url: RedisDsn = Field(..., env='REDIS_URL')
    pool_size: int = Field(10, env='REDIS_POOL_SIZE')
    pool_timeout: int = Field(30, env='REDIS_POOL_TIMEOUT')

    class Config:
        env_prefix = "REDIS_"

class APISettings(BaseSettings):
    """API configuration settings."""
    title: str = Field('Nedlia User Profile Service', env='API_TITLE')
    description: str = Field('User Profile Management Service with Okta Integration', env='API_DESCRIPTION')
    version: str = Field('0.1.0', env='API_VERSION')
    debug: bool = Field(False, env='API_DEBUG')
    docs_url: str = Field('/docs', env='API_DOCS_URL')
    openapi_url: str = Field('/openapi.json', env='API_OPENAPI_URL')

    class Config:
        env_prefix = "API_"

class OktaSettings(BaseSettings):
    """Okta configuration settings."""
    org_url: HttpUrl = Field(..., env='OKTA_ORG_URL')
    client_id: str = Field(..., env='OKTA_CLIENT_ID')
    client_secret: SecretStr = Field(..., env='OKTA_CLIENT_SECRET')
    api_token: SecretStr = Field(..., env='OKTA_API_TOKEN')
    issuer: HttpUrl = Field(..., env='OKTA_ISSUER')
    audience: str = Field('api://default', env='OKTA_AUDIENCE')

    class Config:
        env_prefix = "OKTA_"

class LoggingSettings(BaseSettings):
    """Logging configuration settings."""
    level: str = Field('INFO', env='LOG_LEVEL')
    json_logs: bool = Field(True, env='LOG_JSON_LOGS')

    class Config:
        env_prefix = "LOG_"

class FeatureFlags(BaseSettings):
    """Feature flag settings."""
    metrics_enabled: bool = Field(True, env='METRICS_ENABLED')
    tracing_enabled: bool = Field(True, env='TRACING_ENABLED')
    profile_sync_enabled: bool = Field(True, env='PROFILE_SYNC_ENABLED')
    webhooks_enabled: bool = Field(True, env='WEBHOOKS_ENABLED')

    class Config:
        env_prefix = ""

class Settings(BaseSettings):
    """Application settings."""
    api: APISettings = Field(default_factory=APISettings)
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    okta: OktaSettings = Field(default_factory=OktaSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    features: FeatureFlags = Field(default_factory=FeatureFlags)
    cors_origins: List[str] = Field(["*"], env='CORS_ORIGINS')

    def get_mongodb_settings(self) -> Dict[str, Any]:
        """Get MongoDB connection settings."""
        return {
            "host": self.db.url,
            "db": self.db.name,
            "minPoolSize": self.db.min_pool_size,
            "maxPoolSize": self.db.max_pool_size,
            "maxIdleTimeMS": self.db.max_idle_time_ms,
            "connectTimeoutMS": self.db.connect_timeout_ms,
            "serverSelectionTimeoutMS": self.db.server_selection_timeout_ms,
        }

    class Config:
        env_file = ".env"
        case_sensitive = False

_settings = None

def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
