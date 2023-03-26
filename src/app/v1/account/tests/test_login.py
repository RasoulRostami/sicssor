from src.conftest import client, override_get_settings
from src.db.repository import UserRepository

from .fixtures import *

settings = override_get_settings()
login_url = "/v1/accounts/login/"


def test_login(customer_user):
    repo = UserRepository(settings)
    user = repo.get_user_by_email("smith@yahoo.com")
    assert user.token == None

    data = {"email": "smith@yahoo.com", "password": "QAZwsx123$%^"}
    response = client.post(login_url, json=data)
    assert response.status_code == 200, response.json()
    assert response.json().get("token") is not None
    user = repo.get_user_by_id(user.id)
    assert user.token != None


@pytest.mark.parametrize(
    "data",
    [
        {  # invalid password
            "email": " smith@yahool.com",
            "password": "Qaz123!@#",
        },
        {  # invalid email
            "email": "email@yahoo.com",
            "password": "QAZwsx123$%^",
        },
        {  # required email
            "password": "QAZws123$%^",
        },
        {  # required password
            "email": "smith@yahoo.com",
        },
    ],
)
def test_login_invalid_data(data):
    response = client.post(login_url, json=data)
    assert response.status_code == 422, response.json()
