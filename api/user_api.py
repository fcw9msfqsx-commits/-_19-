from api.base_api import BaseApi


class UserApi(BaseApi):
    def register(self, username, email, password):
        payload = {
            "username": username,
            "email": email,
            "password": password,
        }

        return self.session.post(
            f"{self.base_url}/api/register",
            json=payload,
        )

    def login(self, email, password):
        payload = {
            "email": email,
            "password": password,
        }

        return self.session.post(
            f"{self.base_url}/api/login",
            json=payload,
        )
