import io
import json
import sys
from pathlib import Path

import pytest

from stop_hook import main


def write_review_state(tmp_path: Path, **overrides: object) -> None:
    review_dir = tmp_path / ".auto-review" / "two-sum"
    review_dir.mkdir(parents=True)
    state = {
        "session_id": "session-123",
        "author_agent": "codex",
        "reviewer_agent": "claude",
        "topic": "two-sum",
        "target": ".auto-review/two-sum/target.md",
        "status": "pending",
        "round": 1,
        "max_rounds": 3,
    }
    state.update(overrides)
    (review_dir / "review.json").write_text(json.dumps(state), encoding="utf-8")


def set_hook_input(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    hook_input = json.dumps({"session_id": "session-123", "cwd": str(tmp_path)})
    monkeypatch.setattr(sys, "stdin", io.StringIO(hook_input))


def test_main_when_review_is_pending_then_block_completion(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # Arrange
    write_review_state(tmp_path)
    set_hook_input(monkeypatch, tmp_path)

    # Act
    result = main()

    # Assert
    response = json.loads(capsys.readouterr().out)
    assert result == 0
    assert response["decision"] == "block"
    assert 'auto-review is still pending for "two-sum".' in response["reason"]


def test_main_when_review_is_approved_then_allow_completion(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # Arrange
    write_review_state(tmp_path, status="approved")
    set_hook_input(monkeypatch, tmp_path)

    # Act
    result = main()

    # Assert
    assert result == 0
    assert capsys.readouterr().out == ""


def test_main_when_max_rounds_reached_then_allow_completion(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # Arrange
    write_review_state(tmp_path, round=3, max_rounds=3)
    set_hook_input(monkeypatch, tmp_path)

    # Act
    result = main()

    # Assert
    assert result == 0
    assert capsys.readouterr().out == ""


def test_main_when_session_id_is_missing_then_raise_contract_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    hook_input = json.dumps({"cwd": "/tmp", "hook_event_name": "Stop"})
    monkeypatch.setattr(sys, "stdin", io.StringIO(hook_input))

    # Act & Assert
    with pytest.raises(KeyError):
        main()


def test_main_when_status_is_unexpected_then_return_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    write_review_state(tmp_path, status="rejected")
    set_hook_input(monkeypatch, tmp_path)

    # Act
    result = main()

    # Assert
    assert result == 1
