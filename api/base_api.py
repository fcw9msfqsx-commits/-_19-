import requests


class BaseApi:
    def __init__(self):
        self.base_url = "http://185.240.103.201:8000"
        self.session = requests.Session()
