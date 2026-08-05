#!/usr/bin/env python3

import json
import sys
from pathlib import Path
from typing import Any

ReviewState = dict[str, Any]
ReviewMatch = tuple[Path, ReviewState]


def main() -> int:
    hook_input = read_hook_input()
    session_id = hook_input["session_id"]
    working_directory = hook_input["cwd"]

    project_root = find_project_root(working_directory)
    review_match = find_review_for_session(project_root, session_id)
    if review_match is None:
        return 0

    review_path, review_state = review_match
    status = review_state["status"]
    if status not in {"approved", "pending"}:
        return 1

    if status == "approved" or has_reached_max_review_rounds(review_state):
        return 0

    block_pending_review(review_path, review_state)
    return 0


def read_hook_input() -> ReviewState:
    raw = sys.stdin.read()
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise TypeError("hook input must be a JSON object")
    return payload


def find_project_root(start: str | Path) -> Path:
    current = Path(start).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".auto-review").exists() or (candidate / ".git").exists():
            return candidate
    return current


def find_review_for_session(project_root: Path, session_id: str) -> ReviewMatch | None:
    for path in find_review_files(project_root):
        state = read_json(path)
        if state is not None and state.get("session_id") == session_id:
            return path, state
    return None


def find_review_files(root: Path) -> list[Path]:
    base = root / ".auto-review"
    if not base.exists():
        return []
    return sorted(path for path in base.glob("*/review.json") if path.is_file())


def read_json(path: Path) -> ReviewState | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def has_reached_max_review_rounds(review_state: ReviewState) -> bool:
    round_no = int(review_state["round"])
    max_rounds = int(review_state["max_rounds"])
    return round_no >= max_rounds


def block_pending_review(review_path: Path, review_state: ReviewState) -> None:
    block(build_pending_reason(review_path, review_state))


def build_pending_reason(
    review_path: Path,
    state: ReviewState,
) -> str:
    topic = state.get("topic") or review_path.parent.name
    target = state.get("target") or "target"
    reviewer = state.get("reviewer_agent") or "reviewer"
    author = state.get("author_agent") or "author"
    round_no = state["round"]
    max_rounds = state["max_rounds"]
    response_path = f".auto-review/{topic}/responsed_by_{author}.md"
    return "\n".join(
        [
            f'auto-review is still pending for "{topic}".',
            f"Target: {target}",
            f"Ask {reviewer} to review the updated target, then update {response_path}.",
            f"Run the reviewer session again so the harness can update .auto-review/{topic}/review.json.",
            f"Current round: {round_no}/{max_rounds}.",
        ]
    )


def block(reason: str) -> None:
    print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))


if __name__ == "__main__":
    raise SystemExit(main())
