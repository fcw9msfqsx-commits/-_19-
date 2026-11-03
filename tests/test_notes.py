def test_get_notes_success(notes_api, token):
    response = notes_api.get_notes(token)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_notes_without_token(notes_api):
    response = notes_api.get_notes()

    assert response.status_code == 401


def test_get_notes_invalid_token(notes_api):
    response = notes_api.get_notes("invalid_token")

    assert response.status_code == 403


def test_create_note_success(notes_api, token):
    response = notes_api.create_note(
        title="Test note",
        content="Test content",
        token=token,
    )

    assert response.status_code == 201


def test_create_note_without_token(notes_api):
    response = notes_api.create_note(
        title="Test note",
        content="Test content",
    )

    assert response.status_code == 401


def test_create_note_invalid_token(notes_api):
    response = notes_api.create_note(
        title="Test note",
        content="Test content",
        token="invalid_token",
    )

    assert response.status_code == 403


def test_delete_note_success(notes_api, token):
    create_response = notes_api.create_note(
        title="Note for delete",
        content="Delete me",
        token=token,
    )

    assert create_response.status_code == 201

    notes_response = notes_api.get_notes(token)
    note_id = notes_response.json()[-1]["id"]

    delete_response = notes_api.delete_note(note_id, token)

    assert delete_response.status_code == 200


def test_delete_note_without_token(notes_api, token):
    create_response = notes_api.create_note(
        title="Note without token",
        content="Test content",
        token=token,
    )

    assert create_response.status_code == 201

    notes_response = notes_api.get_notes(token)
    note_id = notes_response.json()[-1]["id"]

    delete_response = notes_api.delete_note(note_id)

    assert delete_response.status_code == 401


def test_delete_note_invalid_token(notes_api, token):
    create_response = notes_api.create_note(
        title="Note invalid token",
        content="Test content",
        token=token,
    )

    assert create_response.status_code == 201

    notes_response = notes_api.get_notes(token)
    note_id = notes_response.json()[-1]["id"]

    delete_response = notes_api.delete_note(
        note_id,
        "invalid_token",
    )

    assert delete_response.status_code == 403

    def test_delete_other_users_note(user_api, notes_api, token, user_data):
        create_response = notes_api.create_note(
            title="Foreign note",
            content="This note belongs to another user",
            token=token,
        )

        assert create_response.status_code == 201

        notes_response = notes_api.get_notes(token)
        note_id = notes_response.json()[-1]["id"]

        second_user = {
            "username": f"second_{user_data['username']}",
            "email": f"second_{user_data['email']}",
            "password": user_data["password"],
        }

        register_response = user_api.register(
            second_user["username"],
            second_user["email"],
            second_user["password"],
        )

        assert register_response.status_code == 201

        login_response = user_api.login(
            second_user["email"],
            second_user["password"],
        )

        assert login_response.status_code == 200

        second_token = login_response.json()["token"]

        delete_response = notes_api.delete_note(
            note_id,
            second_token,
        )

        assert delete_response.status_code == 409
