import uuid

import pytest

from api.notes_api import NotesApi
from api.user_api import UserApi


@pytest.fixture
def user_api():
    return UserApi()


@pytest.fixture
def notes_api():
    return NotesApi()


@pytest.fixture
def user_data():
    unique_id = uuid.uuid4().hex[:8]

    return {
        "username": f"user_{unique_id}",
        "email": f"user_{unique_id}@example.com",
        "password": "Test12345",
    }


@pytest.fixture
def registered_user(user_api, user_data):
    response = user_api.register(
        user_data["username"],
        user_data["email"],
        user_data["password"],
    )

    assert response.status_code == 201

    return user_data


@pytest.fixture
def token(user_api, registered_user):
    response = user_api.login(
        registered_user["email"],
        registered_user["password"],
    )

    assert response.status_code == 200

    return response.json()["token"]
