import pytest
from src.conftest import override_get_settings
from src.db import User
from src.db.repository import UserRepository

settings = override_get_settings()


@pytest.fixture
def customer_user():
    # password = QAZwsx123$%^
    user = User(
        first_name="Tom",
        last_name="Smith",
        email="smith@yahoo.com",
        password="a4ee4d3025a9d7cbfda6cc4b99d8af09bd45441b0622135e619bbb97067a57e7",
        token=None,
    )
    UserRepository(settings).create(user)
    return user
