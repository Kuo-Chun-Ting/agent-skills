#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

from reviewer_contract import build_review_prompt, parse_codex_output


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: new_codex_session.py <prompt_file>", file=sys.stderr)
        return 2

    prompt = build_review_prompt(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = subprocess.run(
        [
            "codex",
            "exec",
            "--skip-git-repo-check",
            "--sandbox",
            "read-only",
            "--json",
            "-",
        ],
        input=prompt,
        text=True,
        capture_output=True,
    )
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    result.check_returncode()

    print(json.dumps(parse_codex_output(result.stdout), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
