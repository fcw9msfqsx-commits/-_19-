from helpers.helper import make_user


class TestUsers:
    def test_register(self, auth):
        user = make_user()
        response = auth.register(**user)

        assert response.status_code == 201, (
            f"Пользователь не зарегистрирован: {response.text}"
        )
        assert response.json()["message"] == "Успешная регистрация!"

    def test_login(self, auth, registered_user):
        response = auth.authenticate(
            registered_user["email"], registered_user["password"]
        )

        assert response.status_code == 200, (
            f"Не удалось войти в систему: {response.text}"
        )
        token = response.json().get("token")
        assert isinstance(token, str), "В ответе нет строкового токена"
        assert token, "Сервер вернул пустой токен"

    def test_login_with_wrong_password(self, auth, registered_user):
        response = auth.authenticate(
            registered_user["email"], "WrongPassword123!"
        )

        assert response.status_code == 401, (
            f"Ожидался отказ в авторизации, получен ответ: {response.text}"
        )
        assert "message" in response.json(), "В ответе нет сообщения об ошибке"

    def test_register_duplicate_email(self, auth, registered_user):
        response = auth.register(**registered_user)

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

        assert response.status_code in (400, 500), (
            f"Получен неожиданный статус: {response.status_code}"
        )
