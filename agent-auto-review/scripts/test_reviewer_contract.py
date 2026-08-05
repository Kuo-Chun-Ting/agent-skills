import json

import pytest

from reviewer_contract import (
    parse_claude_output,
    parse_codex_output,
    parse_helper_output,
)


def test_parse_claude_output_when_review_is_approved_then_return_reviewer_result() -> (
    None
):
    # Arrange
    output = json.dumps(
        {
            "session_id": "claude-session-123",
            "result": '{"status":"approved","review":"Looks good."}',
        }
    )

    # Act
    result = parse_claude_output(output)

    # Assert
    assert result == {
        "session_id": "claude-session-123",
        "status": "approved",
        "review": "Looks good.",
    }


def test_parse_codex_output_when_review_is_pending_then_return_reviewer_result() -> (
    None
):
    # Arrange
    output = "\n".join(
        [
            '{"type":"thread.started","thread_id":"codex-thread-123"}',
            '{"type":"turn.started"}',
            (
                '{"type":"item.completed","item":{"type":"agent_message",'
                '"text":"{\\"status\\":\\"pending\\",\\"review\\":\\"Fix the edge case.\\"}"}}'
            ),
        ]
    )

    # Act
    result = parse_codex_output(output)

    # Assert
    assert result == {
        "session_id": "codex-thread-123",
        "status": "pending",
        "review": "Fix the edge case.",
    }


def test_parse_helper_output_when_status_is_unexpected_then_raise_contract_error() -> (
    None
):
    # Arrange
    output = '{"session_id":"session-123","status":"rejected","review":"No."}'

    # Act & Assert
    with pytest.raises(ValueError, match="unexpected review status"):
        parse_helper_output(output)


def test_parse_helper_output_when_session_id_is_empty_then_raise_contract_error() -> (
    None
):
    # Arrange
    output = '{"session_id":"","status":"approved","review":"Looks good."}'

    # Act & Assert
    with pytest.raises(ValueError, match="session_id"):
        parse_helper_output(output)
