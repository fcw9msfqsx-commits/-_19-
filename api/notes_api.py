from api.base_api import BaseApi


class NotesApi(BaseApi):
    def get_notes(self, token=None):
        headers = self._get_headers(token)

        return self.session.get(
            f"{self.base_url}/api/notes",
            headers=headers,
        )

    def create_note(self, title, content, token=None):
        headers = self._get_headers(token)

        payload = {
            "title": title,
            "content": content,
        }

        return self.session.post(
            f"{self.base_url}/api/notes",
            headers=headers,
            json=payload,
        )

    def delete_note(self, note_id, token=None):
        headers = self._get_headers(token)

        return self.session.delete(
            f"{self.base_url}/api/notes/{note_id}",
            headers=headers,
        )

    @staticmethod
    def _get_headers(token):
        if token is None:
            return {}

        return {
            "Authorization": f"Bearer {token}",
        }
