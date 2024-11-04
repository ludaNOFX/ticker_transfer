import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=f'{os.path.dirname(os.path.abspath(__file__))}/../../.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    POSTGRES_SERVER: str
    # DATABASE_PORT: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@172.19.0.2/{self.DB_NAME}"

settings = Settings()