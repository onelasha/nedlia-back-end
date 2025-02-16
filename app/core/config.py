"""
Core configuration module
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    PROJECT_NAME: str = "Nedlia Backend"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # pylint: disable=too-few-public-methods
    class Config:
        """Pydantic config"""

        case_sensitive = True


settings = Settings()
