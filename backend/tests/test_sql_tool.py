from unittest.mock import MagicMock

from app.agents import sql_tool


def test_query_operations_returns_rows(monkeypatch):
    fake_rows = [
        {
            "site": "NYC-02",
            "timestamp": "2026-09-04T14:00:00",
            "throughput": 7100.0,
            "staffing": 78,
            "downtime_minutes": 35.0,
        }
    ]

    fake_connection = MagicMock()
    fake_connection.execute.return_value.mappings.return_value.all.return_value = (
        fake_rows
    )

    fake_context = MagicMock()
    fake_context.__enter__.return_value = fake_connection
    fake_context.__exit__.return_value = False

    fake_engine = MagicMock()
    fake_engine.connect.return_value = fake_context

    monkeypatch.setattr(sql_tool, "engine", fake_engine)

    result = sql_tool.query_operations("NYC-02")

    assert result == fake_rows
    fake_connection.execute.assert_called_once()
