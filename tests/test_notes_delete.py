class TestNotesDelete:
    def test_delete_note(self, notes_api_with_token, note_for_test):
        response = notes_api_with_token.delete_note(note_for_test["id"])

        assert response.status_code == 200, (
            f"Заметка не удалена: {response.text}"
        )
        assert response.json() == {"message": "Note deleted!"}

    def test_delete_note_without_token(
        self, notes_api_without_token, note_for_test
    ):
        response = notes_api_without_token.delete_note(note_for_test["id"])

        assert response.status_code == 401, (
            f"Ожидался отказ без токена: {response.text}"
        )
        assert response.json() == {"message": "Token is missing!"}

    def test_delete_note_with_invalid_token(
        self, notes_api_with_invalid_token, note_for_test
    ):
        response = notes_api_with_invalid_token.delete_note(note_for_test["id"])

        assert response.status_code == 403, (
            f"Ожидался отказ с неверным токеном: {response.text}"
        )
        assert response.json() == {"message": "Token is invalid or expired!"}

    def test_delete_note_of_another_user(
        self, another_notes_api, note_for_test
    ):
        response = another_notes_api.delete_note(note_for_test["id"])

        assert response.status_code == 409, (
            f"Ожидался отказ при удалении чужой заметки: {response.text}"
        )
        assert "message" in response.json(), "В ответе нет сообщения об ошибке"
