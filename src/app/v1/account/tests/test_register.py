from src.conftest import client, override_get_settings
from src.db.repository import UserRepository
import pytest

valid_data = {
    "email": "new_user@yahoo.com",
    "password": "Pass123@#$",
    "confirm_password": "Pass123@#$",
}
url = "/v1/accounts/register/"


def test_register():
    response = client.post(url, json=valid_data)
    assert response.status_code == 201, response.json()
    assert (
        UserRepository(override_get_settings()).is_email_exists(valid_data["email"])
        == True
    )


def test_duplicate_email():
    response = client.post(url, json=valid_data)
    assert response.status_code == 201, response.json()

    response = client.post(url, json=valid_data)
    assert response.status_code == 422, response.json()


@pytest.mark.parametrize(
    "data",
    [
        {  # invalid email
            "email": "email",
            "password": "Qaz123!@#",
            "confirm_password": "Qaz123!@#",
        },
        {  # invalid confirm password
            "email": "email@yahoo.com",
            "password": "Qaz123!@#",
            "confirm_password": "Qaz123!!!",
        },
        {  # Not strong password
            "email": "email",
            "password": "ssss",
            "confirm_password": "ssss",
        },
        {  # required email
            "password": "Pass123@#$",
            "confirm_password": "Pass123@#$",
        },
        {  # required password
            "email": "email@yahoo.com",
            "confirm_password": "Pass123@#$",
        },
        {  # required confirm password
            "email": "email@yahoo.com",
            "password": "Pass123@#$",
        },
    ],
)
def test_invalid_data(data):
    response = client.post(url, json=data)
    assert response.status_code == 422, response.json()
