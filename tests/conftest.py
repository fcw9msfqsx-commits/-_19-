import os
from uuid import uuid4

import pytest
from dotenv import load_dotenv

from api.notes.notes_api import NotesApi
from api.users.auth import Auth
from helpers.helper_remember import HelperRemember


load_dotenv()


@pytest.fixture(scope="session")
def auth():
    return Auth()


@pytest.fixture(scope="session")
def primary_user_credentials():
    return {
        "email": os.getenv("TEST_EMAIL"),
        "password": os.getenv("TEST_PASSWORD")
    }


@pytest.fixture(scope="session")
def secondary_user_credentials():
    return {
        "email": os.getenv("ANOTHER_TEST_EMAIL"),
        "password": os.getenv("ANOTHER_TEST_PASSWORD")
    }


@pytest.fixture
def registration_user():
    value = uuid4().hex[:10]
    return {
        "email": f"test_{value}@testov.ru",
        "password": "QaAutomation123!",
        "username": f"qa_{value}"
    }


@pytest.fixture(scope="session")
def token(auth, primary_user_credentials):
    return auth.get_token(
        primary_user_credentials["email"],
        primary_user_credentials["password"]
    )


@pytest.fixture(scope="session")
def another_token(auth, secondary_user_credentials):
    return auth.get_token(
        secondary_user_credentials["email"],
        secondary_user_credentials["password"]
    )


@pytest.fixture(scope="session")
def another_token(auth, secondary_user_credentials):
    return auth.get_token(
        secondary_user_credentials["email"],
        secondary_user_credentials["password"]
    )


@pytest.fixture
def notes_api_with_token(token):
    return NotesApi(token=token)


@pytest.fixture
def helper_remember():
    return HelperRemember()


@pytest.fixture
def notes_api_without_token():
    return NotesApi()


@pytest.fixture
def notes_api_with_invalid_token(token):
    return NotesApi(token=f"{token}invalid")


@pytest.fixture
def note_data():
    return {
        "title": f"Тестовая заметка {uuid4().hex[:8]}",
        "content": "Содержимое тестовой заметки"
    }


@pytest.fixture
def create_note(notes_api_with_token, note_data, helper_remember):
    notes_api_with_token.post_note(**note_data)
    helper_remember.remember_note(note_data["title"])


@pytest.fixture
def setup(notes_api_with_token, create_note, helper_remember):
    notes_id = notes_api_with_token.get_note_for_title(
        helper_remember.title
    )["id"]
    return notes_id


@pytest.fixture
def teardown(notes_api_with_token, helper_remember):
    yield
    if helper_remember.title:
        note = notes_api_with_token.get_note_for_title(helper_remember.title)
        if note:
            notes_api_with_token.delete_note(note["id"])


@pytest.fixture
def another_notes_api(another_token):
    return NotesApi(token=another_token)
