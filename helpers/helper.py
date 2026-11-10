from uuid import uuid4


def build_headers(token=None):
    headers = {"accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def make_user():
    value = uuid4().hex
    return {
        "email": f"test_{value[:12]}@testov.ru",
        "password": "QaAutomation123!",
        "username": f"qa_{value[:11]}"
    }
