from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # System Configurations
    PROJECT_NAME: str = "Jakasipul Core: Mobility API"
    ENVIRONMENT: str = "development"

    # MongoDB Configurations
    MONGO_HOST: str
    MONGO_PORT: int = 27017
    MONGO_DB_NAME: str
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str

    @property
    def database_url(self) -> str:
        """Dynamically builds the async MongoDB connection string."""
        return (
            f"mongodb://{self.MONGO_INITDB_ROOT_USERNAME}:"
            f"{self.MONGO_INITDB_ROOT_PASSWORD}@"
            f"{self.MONGO_HOST}:{self.MONGO_PORT}"
        )

    # Automatically loads configurations from a local .env file if it exists
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Instantiated as a global singleton across the codebase
settings = Settings()
