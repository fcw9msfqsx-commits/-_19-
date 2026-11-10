class TestNotesGet:
    def test_get_notes(self, notes_api_with_token, note_for_test):
        response = notes_api_with_token.get_notes()

        assert response.status_code == 200, (
            f"Не удалось получить заметки: {response.text}"
        )
        notes = response.json()
        assert isinstance(notes, list), "В ответе ожидался список заметок"
        assert any(note["id"] == note_for_test["id"] for note in notes), (
            "Созданная заметка не найдена в списке"
        )
        for note in notes:
            assert {"id", "title", "content"}.issubset(note), (
                f"У заметки не хватает обязательных полей: {note}"
            )

    def test_get_notes_without_token(self, notes_api_without_token):
        response = notes_api_without_token.get_notes()

        assert response.status_code == 401, (
            f"Ожидался отказ без токена: {response.text}"
        )
        assert response.json() == {"message": "Token is missing!"}

    def test_get_notes_with_invalid_token(self, notes_api_with_invalid_token):
        response = notes_api_with_invalid_token.get_notes()

        assert response.status_code == 403, (
            f"Ожидался отказ с неверным токеном: {response.text}"
        )
        assert response.json() == {"message": "Token is invalid or expired!"}
