from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SISWORK Backend"
    app_version: str = "0.1.0"
    app_env: str = "development"
    app_debug: bool = True

    api_v1_str: str = "/api/v1"

    db_host: str = "127.0.0.1"
    db_port: int = 5432
    db_name: str = "siswork_db"
    db_user: str = "ruper"
    db_password: str = "demons312es"

    secret_key: str = "change_this_secret_key"
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()