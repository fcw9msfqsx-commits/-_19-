from api.base_api import BaseApi


class NotesApi(BaseApi):
    def __init__(self, token=None):
        super().__init__()
        self.token = token

    def _get_headers(self):
        if self.token is None:
            return {}

        return {
            "Authorization": f"Bearer {self.token}",
        }

    def get_notes(self):
        return self.get(
            "/api/notes",
            headers=self._get_headers(),
        )

    def create_note(self, title, content):
        payload = {
            "title": title,
            "content": content,
        }

        return self.post(
            "/api/notes",
            json=payload,
            headers=self._get_headers(),
        )

    def delete_note(self, note_id):
        return self.delete(
            f"/api/notes/{note_id}",
            headers=self._get_headers(),
        )
