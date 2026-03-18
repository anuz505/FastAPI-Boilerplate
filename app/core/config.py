from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path


ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    app_name: str = "Boilerplate fastapi"
    app_version: str = "1.0.0"
    debug: bool = True
    log_level: str = "INFO"
    port: int = 8000
    description: str = "App description here.."

    postgres_user: str = Field(default="postgres", description="postgres user")
    postgres_password: str = Field(default="root",
                                   description="postgres password")
    postgres_host: str = Field(default="localhost",
                               description="PostgreSQL host")
    postgres_port: int = Field(default=5432, description="PostgreSQL port")
    postgres_db: str = Field(default="Boilerplate",
                             description="PostgreSQL database name")

    @property
    def db_url(self) -> str:
        return (
            (
                f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
                f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
            )
        )
    secret_key: str = Field(description="password hash secret key")
    ALGORITHM: str = Field(description="Algorithm")
    ACCESS_TOKEN_EXPIRES_MINUTES: int = Field(description="Access token expiry date in minutes")
    REFRESH_TOKEN_EXPIRES: int = Field(description="Refresh token expirty date")

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()
