import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_SERVER: str
    DATABASE_PORT: int

    @property
    def db_url(self) -> str:
        user = self.DATABASE_USER
        password = self.DATABASE_PASSWORD
        server = self.DATABASE_SERVER
        port = self.DATABASE_PORT
        db = self.DATABASE_NAME
        return f"mysql+mysqldb://{user}:{password}@{server}:{port}/{db}"

    @property
    def async_db_url(self) -> str:
        user = self.DATABASE_USER
        password = self.DATABASE_PASSWORD
        server = self.DATABASE_SERVER
        port = self.DATABASE_PORT
        db = self.DATABASE_NAME
        return f"mysql+aiomysql://{user}:{password}@{server}:{port}/{db}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


BASE_DIR: str = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
