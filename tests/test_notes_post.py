from uuid import uuid4


class TestNotesPost:
    def test_create_note(self, notes_api_with_token):
        title = f"Список продуктов {uuid4().hex[:8]}"
        content = "Молоко, яйца"

        response = notes_api_with_token.post_note(title=title, content=content)
        assert response.status_code == 201, (
            f"Заметка не создана: {response.text}"
        )
        assert response.json() == {"message": "Заметка создана!"}

        note = notes_api_with_token.get_note_for_title(title)
        assert note is not None, "Созданная заметка не найдена"
        assert note["title"] == title
        assert note["content"] == content
        cleanup_response = notes_api_with_token.delete_note(note["id"])
        assert cleanup_response.status_code == 200, (
            f"Тестовая заметка не удалена: {cleanup_response.text}"
        )

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
