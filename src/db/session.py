from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import Settings


def get_session(settings: Settings):
    engine = create_engine(settings.db_url, pool_pre_ping=True)
    DatabaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return DatabaseSession()
