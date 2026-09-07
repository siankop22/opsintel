from unittest.mock import MagicMock

from app.agents import memory


def test_get_history_returns_latest_messages_in_order(monkeypatch):
    newest = MagicMock()
    newest.role = "assistant"
    newest.content = "Newest message"

    older = MagicMock()
    older.role = "user"
    older.content = "Older message"

    fake_query = MagicMock()
    fake_query.filter.return_value.order_by.return_value.limit.return_value.all.return_value = [
        newest,
        older,
    ]

    fake_db = MagicMock()
    fake_db.query.return_value = fake_query

    fake_session_local = MagicMock(return_value=fake_db)
    monkeypatch.setattr(memory, "SessionLocal", fake_session_local)

    result = memory.get_history("test-session", limit=2)

    assert result == [
        {"role": "user", "content": "Older message"},
        {"role": "assistant", "content": "Newest message"},
    ]

    fake_query.filter.return_value.order_by.return_value.limit.assert_called_once_with(2)
    fake_db.close.assert_called_once()
