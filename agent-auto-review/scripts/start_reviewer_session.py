#!/usr/bin/env python3
import datetime
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from reviewer_contract import ReviewerResult, parse_helper_output

ReviewState = dict[str, Any]


def main() -> int:
    if len(sys.argv) != 4:
        return usage()

    agent = sys.argv[1]
    topic = sys.argv[2]
    prompt_file = Path(sys.argv[3])
    if agent not in {"claude", "codex"}:
        return usage()

    state_file = Path(".auto-review") / topic / "review.json"
    review_state = read_review_state(state_file)
    if agent != review_state["reviewer_agent"]:
        raise ValueError("reviewer agent does not match review state")

    session_id = review_state.get("reviewer_session_id", "")

    helper, helper_args = select_session_helper(
        Path(__file__).resolve().parent,
        agent,
        session_id,
        prompt_file,
    )
    output = run_helper(helper, helper_args)
    reviewer_result = parse_helper_output(output)
    if session_id and reviewer_result["session_id"] != session_id:
        raise ValueError("reviewer session changed during resume")

    write_review_result(state_file, reviewer_result)
    return 0


def select_session_helper(
    script_dir: Path,
    agent: str,
    session_id: str,
    prompt_file: Path,
) -> tuple[Path, list[str]]:
    action = "resume" if session_id else "new"
    helper = script_dir / f"{action}_{agent}_session.py"
    args = [session_id, str(prompt_file)] if session_id else [str(prompt_file)]
    return helper, args


def write_review_result(
    state_file: Path,
    reviewer_result: ReviewerResult,
) -> None:
    state = read_review_state(state_file)
    reviewer_agent = state["reviewer_agent"]
    audit_file = state_file.parent / f"reviewed_by_{reviewer_agent}.md"

    audit_file.write_text(reviewer_result["review"].rstrip() + "\n", encoding="utf-8")
    state["reviewer_session_id"] = reviewer_result["session_id"]
    state["status"] = reviewer_result["status"]
    state["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    state_file.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def run_helper(helper: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["python3", str(helper), *args], text=True, capture_output=True
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    result.check_returncode()
    return result.stdout


def read_review_state(state_file: Path) -> ReviewState:
    return json.loads(state_file.read_text(encoding="utf-8"))


def usage() -> int:
    print(
        "usage: start_reviewer_session.py <claude|codex> <topic> <prompt_file>",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
