class TestUsers:
    def test_register(self, auth, registration_user):
        user = registration_user
        response = auth.register(**user)

        assert response.status_code == 201, (
            f"Пользователь не зарегистрирован: {response.text}"
        )
        assert response.json()["message"] == "Успешная регистрация!"

    def test_login(self, auth, primary_user_credentials):
        response = auth.login(
            primary_user_credentials["email"], primary_user_credentials["password"]
        )

        assert response.status_code == 200, (
            f"Не удалось войти в систему: {response.text}"
        )
        token = response.json().get("token")
        assert isinstance(token, str), "В ответе нет строкового токена"
        assert token, "Сервер вернул пустой токен"

    def test_login_with_wrong_password(self, auth, primary_user_credentials):
        response = auth.login(
            primary_user_credentials["email"], "WrongPassword123!"
        )

        assert response.status_code == 401, (
            f"Ожидался отказ в авторизации, получен ответ: {response.text}"
        )
        assert "message" in response.json(), "В ответе нет сообщения об ошибке"

    def test_register_duplicate_email(self, auth, primary_user_credentials):
        response = auth.register(
            email=primary_user_credentials["email"],
            password=primary_user_credentials["password"],
            username="another_username"
        )

        assert response.status_code == 409, (
            f"Ожидалось сообщение о занятом email: {response.text}"
        )
        assert "message" in response.json(), "В ответе нет сообщения об ошибке"

    def test_register_with_invalid_body(self, auth):
        response = auth.post(
            auth.REGISTER_ENDPOINT,
            json={"email": "invalid@testov.ru"},
            headers=auth.headers
        )

        assert response.status_code == 500, (
            f"Ожидался статус 500, получен {response.status_code}: "
            f"{response.text}"
        )
