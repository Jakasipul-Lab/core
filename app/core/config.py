"""
Configuration module for Jakasipul Core API.
Manages environment variables and application settings using Pydantic.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, model_validator
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration (Maps to PROJECT_NAME and ENVIRONMENT)
    project_name: str = Field(default="Jakasipul Core: Mobility API", validation_alias="project_name")
    environment: str = Field(default="development", validation_alias="environment")
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Individual Database Pieces from your .env
    mongo_host: str = Field(default="localhost")
    mongo_port: int = Field(default=27017)
    mongo_db_name: str = Field(default="jakasipul_mobility")
    mongo_initdb_root_username: Optional[str] = Field(default=None)
    mongo_initdb_root_password: Optional[str] = Field(default=None)
    
    # Calculated Connection URL used by Motor
    mongodb_url: str = ""

    @model_validator(mode="after")
    def assemble_mongo_url(self) -> "Settings":
        """Dynamically builds the full connection string from individual .env values."""
        # If username and password exist, build an authenticated URI
        if self.mongo_initdb_root_username and self.mongo_initdb_root_password:
            self.mongodb_url = (
                f"mongodb://{self.mongo_initdb_root_username}:{self.mongo_initdb_root_password}@"
                f"{self.mongo_host}:{self.mongo_port}/{self.mongo_db_name}?authSource=admin"
            )
        else:
            # Fallback for simple local setups without credentials
            self.mongodb_url = f"mongodb://{self.mongo_host}:{self.mongo_port}/{self.mongo_db_name}"
        return self
    
    # Security
    api_key: Optional[str] = None
    jwt_secret: Optional[str] = None
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        # case_sensitive = False allows MONGO_HOST to match mongo_host automatically
        case_sensitive = False


# Global settings instance
settings = Settings()
