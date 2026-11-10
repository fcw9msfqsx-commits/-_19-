from uuid import uuid4

import pytest

from api.notes.notes_api import NotesApi
from api.users.auth import Auth
from helpers.helper import make_user


@pytest.fixture(scope="session")
def auth():
    return Auth()


@pytest.fixture(scope="session")
def user_data():
    return make_user()


@pytest.fixture(scope="session")
def registered_user(auth, user_data):
    response = auth.register(**user_data)
    assert response.status_code == 201, response.text
    return user_data


@pytest.fixture(scope="session")
def token(auth, registered_user):
    response = auth.authenticate(
        registered_user["email"], registered_user["password"]
    )
    assert response.status_code == 200, response.text
    return response.json()["token"]


@pytest.fixture
def notes_api_with_token(token):
    return NotesApi(token=token)


@pytest.fixture
def notes_api_without_token():
    return NotesApi()


@pytest.fixture
def notes_api_with_invalid_token(token):
    return NotesApi(token=f"{token}invalid")


@pytest.fixture
def note_for_test(notes_api_with_token):
    title = f"Тестовая заметка {uuid4().hex[:8]}"
    content = "Содержимое тестовой заметки"
    response = notes_api_with_token.post_note(title=title, content=content)
    assert response.status_code == 201, response.text
    note = notes_api_with_token.get_note_for_title(title)
    assert note is not None
    yield note
    cleanup_response = notes_api_with_token.delete_note(note["id"])
    assert cleanup_response.status_code in (200, 404), cleanup_response.text


@pytest.fixture
def another_notes_api(auth):
    another_user = make_user()
    register_response = auth.register(**another_user)
    assert register_response.status_code == 201, register_response.text
    token_response = auth.authenticate(
        another_user["email"], another_user["password"]
    )
    assert token_response.status_code == 200, token_response.text
    return NotesApi(token=token_response.json()["token"])
