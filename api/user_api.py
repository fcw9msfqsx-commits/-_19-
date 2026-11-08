from api.base_api import BaseApi


class UserApi(BaseApi):
    def register(self, username, email, password):
        payload = {
            "username": username,
            "email": email,
            "password": password,
        }

        return self.post(
            "/api/register",
            json=payload,
        )

    def login(self, email, password):
        payload = {
            "email": email,
            "password": password,
        }

        return self.post(
            "/api/login",
            json=payload,
        )

    def get_token(self, email, password):
        response = self.login(email, password)
        return response.json()["token"]
