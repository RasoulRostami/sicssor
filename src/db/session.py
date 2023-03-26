from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import Settings


def get_session(settings: Settings):
    engine = create_engine(settings.db_url, pool_pre_ping=True, echo=False)
    DatabaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return DatabaseSession()


def get_async_session(settings: Settings) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(settings.async_db_url, echo=False)
    return async_sessionmaker(engine, expire_on_commit=False)
