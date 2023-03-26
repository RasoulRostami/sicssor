import asyncio
import pytest
from src.conftest import override_get_settings
from src.db import User
from src.db.repository import UserRepository

settings = override_get_settings()


@pytest.fixture
def user_tom():
    # password = QAZwsx123$%^
    user = User(
        first_name="Tom",
        last_name="Smith",
        email="smith@yahoo.com",
        password="a4ee4d3025a9d7cbfda6cc4b99d8af09bd45441b0622135e619bbb97067a57e7",
        token=None,
    )
    return UserRepository(settings).create(user)


@pytest.fixture
def user_jack():
    # password = QAZwsx123$%^
    user = User(
        first_name="Jack",
        last_name="Wine",
        email="wine@yahoo.com",
        password="a4ee4d3025a9d7cbfda6cc4b99d8af09bd45441b0622135e619bbb97067a57e7",
        token="e37ed891-55d0-4807-a9ca-b43bfa08e325",
    )
    return UserRepository(settings).create(user)


def user_jimin():
    pass
