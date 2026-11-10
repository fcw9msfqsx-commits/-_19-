import requests


class BaseApi:
    base_url = "http://185.240.103.201:8000"

    def get(self, endpoint, headers=None, **kwargs):
        return requests.get(
            f"{self.base_url}/{endpoint}",
            headers=headers,
            **kwargs
        )

    def post(self, endpoint, json=None, headers=None, **kwargs):
        return requests.post(
            f"{self.base_url}/{endpoint}",
            json=json,
            headers=headers,
            **kwargs
        )

    def delete(self, endpoint, headers=None, **kwargs):
        return requests.delete(
            f"{self.base_url}/{endpoint}",
            headers=headers,
            **kwargs
        )
