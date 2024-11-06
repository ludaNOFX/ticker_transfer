import os
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=f'{os.path.dirname(os.path.abspath(__file__))}/../../.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    # DATABASE_PORT: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@localhost:5432/{self.DB_NAME}"

settings = Settings() # type: ignore