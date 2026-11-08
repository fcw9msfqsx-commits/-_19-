def test_login_success(user_api, user1_data):
    response = user_api.login(
        user1_data["email"],
        user1_data["password"],
    )

    assert response.status_code == 200
    assert "token" in response.json()


def test_login_invalid_credentials(user_api, user1_data):
    response = user_api.login(
        user1_data["email"],
        "wrong_password",
    )

    assert response.status_code == 401
