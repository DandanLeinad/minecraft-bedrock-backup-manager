#!/usr/bin/env python3
"""DCO check for pre-push hook - validates all commits have Signed-off-by trailer."""

import subprocess
import sys


def run_git_log(*args):
    result = subprocess.run(["git", "log", *args], capture_output=True, text=True)
    return result.stdout.strip()


def main():
    commits_output = run_git_log("--oneline", "@{push}..HEAD")
    if not commits_output:
        commits_output = run_git_log("--oneline", "HEAD")
        if not commits_output:
            return 0

    for line in commits_output.splitlines():
        if not line:
            continue
        hash_ = line.split()[0]
        msg = " ".join(line.split()[1:])
        trailers = run_git_log("-1", "--format=%(trailers)", hash_)
        if "Signed-off-by:" not in trailers:
            print(f"Commit {hash_} ({msg}) missing Signed-off-by")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
