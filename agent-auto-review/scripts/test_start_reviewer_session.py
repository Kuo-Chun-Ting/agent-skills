import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

import start_reviewer_session
from start_reviewer_session import select_session_helper, write_review_result


def test_select_session_helper_when_session_id_is_empty_then_select_new_helper(
    tmp_path: Path,
) -> None:
    # Arrange
    prompt_file = tmp_path / "prompt.md"

    # Act
    helper, args = select_session_helper(tmp_path, "claude", "", prompt_file)

    # Assert
    assert helper == tmp_path / "new_claude_session.py"
    assert args == [str(prompt_file)]


def test_select_session_helper_when_session_id_exists_then_select_resume_helper(
    tmp_path: Path,
) -> None:
    # Arrange
    prompt_file = tmp_path / "prompt.md"

    # Act
    helper, args = select_session_helper(
        tmp_path,
        "codex",
        "codex-thread-123",
        prompt_file,
    )

    # Assert
    assert helper == tmp_path / "resume_codex_session.py"
    assert args == ["codex-thread-123", str(prompt_file)]


def test_write_review_result_when_review_is_approved_then_update_audit_and_state(
    tmp_path: Path,
) -> None:
    # Arrange
    review_dir = tmp_path / ".auto-review" / "three-sum"
    review_dir.mkdir(parents=True)
    state_file = review_dir / "review.json"
    state_file.write_text(
        json.dumps(
            {
                "reviewer_agent": "claude",
                "reviewer_session_id": "",
                "status": "pending",
            }
        ),
        encoding="utf-8",
    )
    reviewer_result = {
        "session_id": "claude-session-123",
        "status": "approved",
        "review": "Looks good.",
    }

    # Act
    write_review_result(state_file, reviewer_result)

    # Assert
    state = json.loads(state_file.read_text(encoding="utf-8"))
    assert state["reviewer_session_id"] == "claude-session-123"
    assert state["status"] == "approved"
    assert state["updated_at"]
    assert (review_dir / "reviewed_by_claude.md").read_text(
        encoding="utf-8"
    ) == "Looks good.\n"


def test_main_when_helper_approves_review_then_persist_audit_and_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    state_file = write_review_state(tmp_path)
    prompt_file = tmp_path / "prompt.md"
    prompt_file.write_text("Review this target.", encoding="utf-8")
    helper_output = json.dumps(
        {
            "session_id": "claude-session-123",
            "status": "approved",
            "review": "Looks good.",
        }
    )
    mock_run_helper = MagicMock(return_value=helper_output)
    monkeypatch.setattr(start_reviewer_session, "run_helper", mock_run_helper)
    monkeypatch.setattr(
        sys,
        "argv",
        ["start_reviewer_session.py", "claude", "three-sum", str(prompt_file)],
    )
    monkeypatch.chdir(tmp_path)

    # Act
    exit_code = start_reviewer_session.main()

    # Assert
    state = json.loads(state_file.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert state["status"] == "approved"
    assert state["reviewer_session_id"] == "claude-session-123"
    assert (state_file.parent / "reviewed_by_claude.md").read_text(
        encoding="utf-8"
    ) == "Looks good.\n"


def test_main_when_agent_differs_from_review_state_then_raise_contract_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    write_review_state(tmp_path, reviewer_agent="codex")
    prompt_file = tmp_path / "prompt.md"
    prompt_file.write_text("Review this target.", encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["start_reviewer_session.py", "claude", "three-sum", str(prompt_file)],
    )
    monkeypatch.chdir(tmp_path)

    # Act & Assert
    with pytest.raises(ValueError, match="reviewer agent"):
        start_reviewer_session.main()


def test_main_when_resume_returns_different_session_then_raise_contract_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    state_file = write_review_state(
        tmp_path,
        reviewer_session_id="claude-session-123",
    )
    prompt_file = tmp_path / "prompt.md"
    prompt_file.write_text("Review this target again.", encoding="utf-8")
    helper_output = json.dumps(
        {
            "session_id": "claude-session-456",
            "status": "approved",
            "review": "Looks good.",
        }
    )
    mock_run_helper = MagicMock(return_value=helper_output)
    monkeypatch.setattr(start_reviewer_session, "run_helper", mock_run_helper)
    monkeypatch.setattr(
        sys,
        "argv",
        ["start_reviewer_session.py", "claude", "three-sum", str(prompt_file)],
    )
    monkeypatch.chdir(tmp_path)

    # Act & Assert
    with pytest.raises(ValueError, match="reviewer session"):
        start_reviewer_session.main()

    state = json.loads(state_file.read_text(encoding="utf-8"))
    assert state["reviewer_session_id"] == "claude-session-123"
    assert state["status"] == "pending"


def write_review_state(
    tmp_path: Path,
    reviewer_agent: str = "claude",
    reviewer_session_id: str = "",
) -> Path:
    review_dir = tmp_path / ".auto-review" / "three-sum"
    review_dir.mkdir(parents=True)
    state_file = review_dir / "review.json"
    state_file.write_text(
        json.dumps(
            {
                "reviewer_agent": reviewer_agent,
                "reviewer_session_id": reviewer_session_id,
                "status": "pending",
            }
        ),
        encoding="utf-8",
    )
    return state_file
