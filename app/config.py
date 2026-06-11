from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):

    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_HOURS: int

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()