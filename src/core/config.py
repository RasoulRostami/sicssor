from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    PROJECT_NAME: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_SERVER: str
    DATABASE_PORT: int

    BASE_DIR: str = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
