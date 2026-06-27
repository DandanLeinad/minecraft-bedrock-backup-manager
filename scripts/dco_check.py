#!/usr/bin/env python3
"""DCO check for pre-push hook."""

from __future__ import annotations

import subprocess


def git_log(*args: str) -> str:
    result = subprocess.run(
        ["git", "log", *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


def main() -> int:
    commits = git_log("--oneline", "@{push}..HEAD")

    if not commits:
        commits = git_log("--oneline", "HEAD")

    if not commits:
        return 0

    for line in commits.splitlines():
        commit_hash, *message = line.split()

        signed_off = git_log(
            "-1",
            "--format=%(trailers:key=Signed-off-by)",
            commit_hash,
        )

        if not signed_off:
            print(f"❌ Commit {commit_hash} ({' '.join(message)}) is missing Signed-off-by")
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
