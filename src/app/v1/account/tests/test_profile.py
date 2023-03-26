from src.conftest import client, override_get_settings
from src.db.repository import UserRepository

from .fixtures import *

settings = override_get_settings()
profile_url = "/v1/accounts/profile"
repo = UserRepository(settings)


def test_get_profile_detail(user_jack):
    response = client.get(
        profile_url, headers={"Authorization": f"Bearer {user_jack.token}"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "first_name": "Jack",
        "last_name": "Wine",
        "birthday": None,
        "bio": None,
        "avatar": None,
    }


@pytest.mark.parametrize(
    "data",
    [
        {"first_name": "tom"},
        {"last_name": "tomi"},
        {"birthday": "2020-02-02"},
        {"bio": "Hello!"},
    ],
)
def test_update_profile(user_jack, data):
    auth_header = {"Authorization": f"Bearer {user_jack.token}"}
    response = client.patch(profile_url, json=data, headers=auth_header)
    assert response.status_code == 200, response.json()
    key = list(data.keys())[0]
    value = list(data.values())[0]
    assert response.json()[key] == value
