from types import SimpleNamespace

from app.agents import investigator


def test_investigate_returns_observability_metrics(monkeypatch):
    response = SimpleNamespace(
        output=[],
        output_text="Investigation complete.",
    )

    monkeypatch.setattr(
        investigator.client.responses,
        "create",
        lambda **kwargs: response,
    )

    monkeypatch.setattr(
        investigator,
        "get_history",
        lambda session_id: [],
    )

    monkeypatch.setattr(
        investigator,
        "save_message",
        lambda *args, **kwargs: None,
    )

    times = iter([10.0, 10.25])

    monkeypatch.setattr(
        investigator.time,
        "perf_counter",
        lambda: next(times),
    )

    result = investigator.investigate(
        "What happened?",
        session_id="test-session",
    )

    assert result["answer"] == "Investigation complete."
    assert result["session_id"] == "test-session"
    assert result["tool_call_count"] == 0
    assert result["latency_ms"] == 250.0
