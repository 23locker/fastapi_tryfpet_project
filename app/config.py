from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Configure DB"""

    DB_HOST: str = Field(default="localhost", alias="DB_HOST")
    DB_PORT: int = Field(default=5433, alias="DB_PORT")
    DB_USER: str = Field(default="postgres", alias="DB_USER")
    DB_PASSWORD: str = Field(default="postgres", alias="DB_PASSWORD")
    DB_NAME: str = Field(default="finflow", alias="DB_NAME")

    @property
    def async_url(self) -> str:
        """URL для asyncpg (FastAPI)"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def sync_url(self) -> str:
        """URL для psycopg2 (Alembic миграции)"""
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = {
        "env_file": ".env",
        "env_prefix": "",
        "extra": "ignore",
    }


class SecuritySettings(BaseSettings):
    """Security settings"""

    secret_key: str = Field(default="dev-secret-key", alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    model_config = {
        "env_file": ".env",
        "env_prefix": "",
        "extra": "ignore",
    }


class AppSettings(BaseSettings):
    debug: bool = Field(default=True, alias="DEBUG")
    title: str = "FinFlow API"
    version: str = "0.1.0"
    description: str = "Microservice banking application"
    api_v1_prefix: str = "/api/v1"

    database: DatabaseSettings = DatabaseSettings()
    security: SecuritySettings = SecuritySettings()

    model_config = {
        "env_file": ".env",
        "env_prefix": "",
        "extra": "ignore",
    }


settings = AppSettings()
