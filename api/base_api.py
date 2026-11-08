import requests


class BaseApi:
    def __init__(self):
        self.base_url = "http://185.240.103.201:8000"
        self.session = requests.Session()

    def get(self, endpoint, headers=None):
        return self.session.get(
            f"{self.base_url}{endpoint}",
            headers=headers,
        )

    def post(self, endpoint, json=None, headers=None):
        return self.session.post(
            f"{self.base_url}{endpoint}",
            json=json,
            headers=headers,
        )

    def delete(self, endpoint, headers=None):
        return self.session.delete(
            f"{self.base_url}{endpoint}",
            headers=headers,
        )
