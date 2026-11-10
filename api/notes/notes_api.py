from api.base_api import BaseApi
from helpers import helper


class NotesApi(BaseApi):
    ENDPOINT = "api/notes"

    def __init__(self, token=None):
        self.token = token
        self.headers = helper.build_headers(self.token)

    def get_notes(self):
        response = self.get(self.ENDPOINT, self.headers)
        return response

    def post_note(self, content, title):
        note = {"title": title, "content": content}
        response = self.post(
            endpoint=self.ENDPOINT,
            headers=self.headers,
            json=note
        )
        return response

    def delete_note(self, note_id):
        response = self.delete(
            endpoint=f"{self.ENDPOINT}/{note_id}",
            headers=self.headers
        )
        return response

    def get_note_for_title(self, title):
        for note in self.get_notes().json():
            if note["title"] == title:
                return note
        return None
