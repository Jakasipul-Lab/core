"""
Configuration module for Jakasipul Core API.
Manages environment variables and application settings using Pydantic.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    app_name: str = "Jakasipul Core"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database Configuration
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "jakasipul"
    
    # Security
    api_key: Optional[str] = None
    jwt_secret: Optional[str] = None
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
