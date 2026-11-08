from uuid import uuid4


def test_get_notes_success(notes_api):
    response = notes_api.get_notes()

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_notes_without_token(notes_api_without_token):
    response = notes_api_without_token.get_notes()

    assert response.status_code == 401


def test_get_notes_invalid_token(notes_api_invalid_token):
    response = notes_api_invalid_token.get_notes()

    assert response.status_code == 403


def test_create_note_success(notes_api, note_for_create_test):
    response = notes_api.create_note(
        title=note_for_create_test["title"],
        content=note_for_create_test["content"],
    )

    assert response.status_code == 201


def test_create_note_without_token(notes_api_without_token):
    response = notes_api_without_token.create_note(
        title=f"Test note {uuid4()}",
        content="Test content",
    )

    assert response.status_code == 401


def test_create_note_invalid_token(notes_api_invalid_token):
    response = notes_api_invalid_token.create_note(
        title=f"Test note {uuid4()}",
        content="Test content",
    )

    assert response.status_code == 403


def test_delete_note_success(notes_api, created_note):
    response = notes_api.delete_note(created_note)

    assert response.status_code == 200


def test_delete_note_without_token(
    notes_api_without_token,
    created_note_with_cleanup,
):
    response = notes_api_without_token.delete_note(
        created_note_with_cleanup
    )

    assert response.status_code == 401


def test_delete_note_invalid_token(
    notes_api_invalid_token,
    created_note_with_cleanup,
):
    response = notes_api_invalid_token.delete_note(
        created_note_with_cleanup
    )

    assert response.status_code == 403


def test_delete_other_users_note(
    second_user_notes_api,
    created_note_with_cleanup,
):
    response = second_user_notes_api.delete_note(
        created_note_with_cleanup
    )

    assert response.status_code == 409
