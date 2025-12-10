from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Configure DB"""

    host: str = Field(default="localhost", alias="DB_HOST")
    port: int = Field(default=5433, alias="DB_PORT")
    user: str = Field(default="postgres", alias="DB_USER")
    password: str = Field(default="postgres", alias="DB_PASSWORD")
    name: str = Field(default="finflow", alias="DB_NAME")

    @property
    def async_url(self) -> str:
        """URL для asyncpg (FastAPI)"""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @property
    def sync_url(self) -> str:
        """URL для psycopg2 (Alembic миграции)"""
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    class Config:
        env_file = ".env"


class SecuritySettings(BaseSettings):
    """Security settings"""

    secret_key: str = Field(default="dev-secret-key", alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    class Config:
        env_file = ".env"


class AppSettings(BaseSettings):
    debug: bool = Field(default=True, alias="DEBUG")
    title: str = "FinFlow API"
    version: str = "0.1.0"
    description: str = "Microservice banking application"
    api_v1_prefix: str = "/api/v1"

    database: DatabaseSettings = DatabaseSettings()
    security: SecuritySettings = SecuritySettings()

    class Config:
        env_file = ".env"


settings = AppSettings()
