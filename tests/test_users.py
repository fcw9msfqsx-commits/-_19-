def test_register_success(user_api, user_data):
    response = user_api.register(
        user_data["username"],
        user_data["email"],
        user_data["password"],
    )

    assert response.status_code == 201


def test_register_bad_request(user_api):
    response = user_api.session.post(
        f"{user_api.base_url}/api/register",
        data="{",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 400


def test_register_existing_email(user_api, registered_user):
    response = user_api.register(
        registered_user["username"],
        registered_user["email"],
        registered_user["password"],
    )

    assert response.status_code == 409


def test_login_success(user_api, registered_user):
    response = user_api.login(
        registered_user["email"],
        registered_user["password"],
    )

    assert response.status_code == 200
    assert "token" in response.json()


def test_login_invalid_credentials(user_api, registered_user):
    response = user_api.login(
        registered_user["email"],
        "WrongPassword123",
    )

    assert response.status_code == 401
