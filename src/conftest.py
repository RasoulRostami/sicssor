import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from core.config import BASE_DIR

sys.path.append(BASE_DIR)


from src.core import get_settings
from src.db import Base
from src.db.session import get_session
from src.main import app


def override_get_settings():
    settings = get_settings()
    settings.DATABASE_NAME = f"test_{settings.DATABASE_NAME}"
    return settings


app.dependency_overrides[get_settings] = override_get_settings


client = TestClient(app)


@pytest.fixture
def create_tables():
    url = override_get_settings().db_url
    engine = create_engine(url, pool_pre_ping=True)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def clear_tables():
    session = get_session(override_get_settings())
    for model in Base.__subclasses__():
        session.query(model).delete()
        session.commit()


@pytest.fixture(autouse=True)
def init(create_tables, clear_tables):
    pass
