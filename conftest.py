import os
from uuid import uuid4

import pytest
from dotenv import load_dotenv

from api.notes_api import NotesApi
from api.user_api import UserApi


load_dotenv()


@pytest.fixture
def user_api():
    return UserApi()


@pytest.fixture
def user1_data():
    return {
        "username": os.getenv("USER1_USERNAME"),
        "email": os.getenv("USER1_EMAIL"),
        "password": os.getenv("USER1_PASSWORD"),
    }


@pytest.fixture
def user2_data():
    return {
        "username": os.getenv("USER2_USERNAME"),
        "email": os.getenv("USER2_EMAIL"),
        "password": os.getenv("USER2_PASSWORD"),
    }


@pytest.fixture
def token(user_api, user1_data):
    return user_api.get_token(
        user1_data["email"],
        user1_data["password"],
    )


@pytest.fixture
def second_token(user_api, user2_data):
    return user_api.get_token(
        user2_data["email"],
        user2_data["password"],
    )


@pytest.fixture
def notes_api(token):
    return NotesApi(token)


@pytest.fixture
def notes_api_without_token():
    return NotesApi()


@pytest.fixture
def notes_api_invalid_token():
    return NotesApi("invalid_token")


@pytest.fixture
def second_user_notes_api(second_token):
    return NotesApi(second_token)


@pytest.fixture
def created_note(notes_api):
    title = f"Test note {uuid4()}"
    content = "Test content"

    notes_api.create_note(title, content)

    notes = notes_api.get_notes().json()
    note_id = next(
        note["id"]
        for note in notes
        if note["title"] == title
    )

    yield note_id


@pytest.fixture
def created_note_with_cleanup(notes_api):
    title = f"Test note {uuid4()}"
    content = "Test content"

    notes_api.create_note(title, content)

    notes = notes_api.get_notes().json()
    note_id = next(
        note["id"]
        for note in notes
        if note["title"] == title
    )

    yield note_id

    notes = notes_api.get_notes().json()

    if any(note["id"] == note_id for note in notes):
        notes_api.delete_note(note_id)


@pytest.fixture
def note_for_create_test(notes_api):
    title = f"Test note {uuid4()}"
    content = "Test content"

    yield {
        "title": title,
        "content": content,
    }

    notes = notes_api.get_notes().json()

    note = next(
        (
            note
            for note in notes
            if note["title"] == title
        ),
        None,
    )

    if note is not None:
        notes_api.delete_note(note["id"])
