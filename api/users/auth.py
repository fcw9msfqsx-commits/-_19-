from api.base_api import BaseApi


class Auth(BaseApi):
    LOGIN_ENDPOINT = "api/login"
    REGISTER_ENDPOINT = "api/register"

    def __init__(self):
        self.headers = {"accept": "application/json"}

    def register(self, email, password, username):
        user = {
            "email": email,
            "password": password,
            "username": username
        }
        return self.post(
            self.REGISTER_ENDPOINT,
            json=user,
            headers=self.headers
        )

    def authenticate(self, email, password):
        user = {"email": email, "password": password}
        return self.post(
            self.LOGIN_ENDPOINT,
            json=user,
            headers=self.headers
        )

    def get_token(self, email, password):
        response = self.authenticate(email, password)
        return response.json()["token"]
