class TestNotesPost:
    def test_create_note(
            self, notes_api_with_token, note_data, teardown, helper_remember
    ):
        helper_remember.remember_note(note_data["title"])

        response = notes_api_with_token.post_note(**note_data)

        assert response.status_code == 201, (
            f"Заметка не создана: {response.text}"
        )
        assert response.json() == {"message": "Заметка создана!"}

        note = notes_api_with_token.get_note_for_title(note_data["title"])
        assert note is not None, "Созданная заметка не найдена"
        assert note["title"] == note_data["title"]
        assert note["content"] == note_data["content"]

    def test_create_note_without_token(self, notes_api_without_token):
        response = notes_api_without_token.post_note(
            title="Без токена", content="Тест"
        )

        assert response.status_code == 401, (
            f"Ожидался отказ без токена: {response.text}"
        )
        assert response.json() == {"message": "Token is missing!"}

    def test_create_note_with_invalid_token(self, notes_api_with_invalid_token):
        response = notes_api_with_invalid_token.post_note(
            title="Неверный токен", content="Тест"
        )

        assert response.status_code == 403, (
            f"Ожидался отказ с неверным токеном: {response.text}"
        )
        assert response.json() == {"message": "Token is invalid or expired!"}
