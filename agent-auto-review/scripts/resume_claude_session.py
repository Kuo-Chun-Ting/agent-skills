#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

from reviewer_contract import build_review_prompt, parse_claude_output


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "usage: resume_claude_session.py <session_id> <prompt_file>",
            file=sys.stderr,
        )
        return 2

    session_id = sys.argv[1]
    prompt = build_review_prompt(Path(sys.argv[2]).read_text(encoding="utf-8"))
    result = subprocess.run(
        [
            "claude",
            "--resume",
            session_id,
            "-p",
            "--output-format",
            "json",
            "--tools=",
            prompt,
        ],
        text=True,
        capture_output=True,
    )
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    result.check_returncode()

    print(json.dumps(parse_claude_output(result.stdout), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
