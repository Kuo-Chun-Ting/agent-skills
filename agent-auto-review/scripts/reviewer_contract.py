import json
from typing import Any, Literal, TypedDict, cast

ReviewStatus = Literal["approved", "pending"]


class ReviewerResult(TypedDict):
    session_id: str
    status: ReviewStatus
    review: str


def build_review_prompt(prompt: str) -> str:
    contract = "\n".join(
        [
            "Return exactly one JSON object and no markdown.",
            'Allowed status values are "approved" and "pending".',
            'JSON shape: {"status":"approved","review":"review text"}',
            "Do not create, modify, or delete files.",
        ]
    )
    return f"{prompt.rstrip()}\n\n{contract}\n"


def parse_claude_output(output: str) -> ReviewerResult:
    cli_result = json.loads(output)
    return _parse_review_payload(cli_result["session_id"], cli_result["result"])


def parse_codex_output(output: str) -> ReviewerResult:
    session_id = ""
    review_payload = ""

    for event in _parse_json_lines(output):
        if event.get("type") == "thread.started":
            session_id = event["thread_id"]

        item = event.get("item", {})
        if (
            event.get("type") == "item.completed"
            and item.get("type") == "agent_message"
        ):
            review_payload = item["text"]

    if not review_payload:
        raise KeyError("agent_message")
    return _parse_review_payload(session_id, review_payload)


def parse_helper_output(output: str) -> ReviewerResult:
    lines = [line for line in output.splitlines() if line.strip()]
    if not lines:
        raise ValueError("helper output must not be empty")
    return _validate_reviewer_result(json.loads(lines[-1]))


def _parse_json_lines(output: str) -> list[dict[str, Any]]:
    return [json.loads(line) for line in output.splitlines() if line.strip()]


def _parse_review_payload(session_id: str, payload: str) -> ReviewerResult:
    review = json.loads(payload)
    return _validate_reviewer_result(
        {
            "session_id": session_id,
            "status": review["status"],
            "review": review["review"],
        }
    )


def _validate_reviewer_result(result: object) -> ReviewerResult:
    if not isinstance(result, dict):
        raise TypeError("reviewer result must be a JSON object")

    session_id = result.get("session_id")
    status = result.get("status")
    review = result.get("review")

    if not isinstance(session_id, str) or not session_id:
        raise ValueError("session_id must not be empty")
    if status not in {"approved", "pending"}:
        raise ValueError(f"unexpected review status: {status}")
    if not isinstance(review, str) or not review.strip():
        raise ValueError("review must not be empty")

    return {
        "session_id": session_id,
        "status": cast(ReviewStatus, status),
        "review": review,
    }
