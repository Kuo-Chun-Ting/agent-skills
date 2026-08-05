import json
import sys
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import MagicMock

import pytest

import new_claude_session
import new_codex_session
import resume_claude_session
import resume_codex_session


def test_new_claude_main_when_review_succeeds_then_disable_tools_and_print_result(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # Arrange
    prompt_file = tmp_path / "prompt.md"
    prompt_file.write_text("Review this target.", encoding="utf-8")
    cli_output = json.dumps(
        {
            "session_id": "claude-session-123",
            "result": '{"status":"approved","review":"Looks good."}',
        }
    )
    mock_run = MagicMock(return_value=CompletedProcess([], 0, cli_output, ""))
    monkeypatch.setattr(new_claude_session.subprocess, "run", mock_run)
    monkeypatch.setattr(sys, "argv", ["new_claude_session.py", str(prompt_file)])

    # Act
    exit_code = new_claude_session.main()

    # Assert
    command = mock_run.call_args.args[0]
    assert command[:5] == ["claude", "-p", "--output-format", "json", "--tools="]
    assert exit_code == 0
    assert json.loads(capsys.readouterr().out.splitlines()[-1]) == {
        "session_id": "claude-session-123",
        "status": "approved",
        "review": "Looks good.",
    }


def test_resume_claude_main_when_review_succeeds_then_return_same_contract(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # Arrange
    prompt_file = tmp_path / "prompt.md"
    prompt_file.write_text("Review this target again.", encoding="utf-8")
    cli_output = json.dumps(
        {
            "session_id": "claude-session-123",
            "result": '{"status":"pending","review":"Fix the edge case."}',
        }
    )
    mock_run = MagicMock(return_value=CompletedProcess([], 0, cli_output, ""))
    monkeypatch.setattr(resume_claude_session.subprocess, "run", mock_run)
    monkeypatch.setattr(
        sys,
        "argv",
        ["resume_claude_session.py", "claude-session-123", str(prompt_file)],
    )

    # Act
    exit_code = resume_claude_session.main()

    # Assert
    command = mock_run.call_args.args[0]
    assert command[:7] == [
        "claude",
        "--resume",
        "claude-session-123",
        "-p",
        "--output-format",
        "json",
        "--tools=",
    ]
    assert exit_code == 0
    assert json.loads(capsys.readouterr().out.splitlines()[-1])["status"] == "pending"


def test_new_codex_main_when_review_succeeds_then_use_read_only_sandbox(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # Arrange
    prompt_file = tmp_path / "prompt.md"
    prompt_file.write_text("Review this target.", encoding="utf-8")
    cli_output = build_codex_output("approved", "Looks good.")
    mock_run = MagicMock(return_value=CompletedProcess([], 0, cli_output, ""))
    monkeypatch.setattr(new_codex_session.subprocess, "run", mock_run)
    monkeypatch.setattr(sys, "argv", ["new_codex_session.py", str(prompt_file)])

    # Act
    exit_code = new_codex_session.main()

    # Assert
    assert mock_run.call_args.args[0] == [
        "codex",
        "exec",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
        "--json",
        "-",
    ]
    assert exit_code == 0
    assert (
        json.loads(capsys.readouterr().out.splitlines()[-1])["session_id"]
        == "codex-thread-123"
    )


def test_resume_codex_main_when_review_succeeds_then_return_same_contract(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # Arrange
    prompt_file = tmp_path / "prompt.md"
    prompt_file.write_text("Review this target again.", encoding="utf-8")
    cli_output = build_codex_output("pending", "Fix the edge case.")
    mock_run = MagicMock(return_value=CompletedProcess([], 0, cli_output, ""))
    monkeypatch.setattr(resume_codex_session.subprocess, "run", mock_run)
    monkeypatch.setattr(
        sys,
        "argv",
        ["resume_codex_session.py", "codex-thread-123", str(prompt_file)],
    )

    # Act
    exit_code = resume_codex_session.main()

    # Assert
    assert mock_run.call_args.args[0] == [
        "codex",
        "exec",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
        "--json",
        "resume",
        "codex-thread-123",
        "-",
    ]
    assert exit_code == 0
    assert json.loads(capsys.readouterr().out.splitlines()[-1])["status"] == "pending"


def build_codex_output(status: str, review: str) -> str:
    review_payload = json.dumps({"status": status, "review": review})
    return "\n".join(
        [
            '{"type":"thread.started","thread_id":"codex-thread-123"}',
            json.dumps(
                {
                    "type": "item.completed",
                    "item": {"type": "agent_message", "text": review_payload},
                }
            ),
        ]
    )
