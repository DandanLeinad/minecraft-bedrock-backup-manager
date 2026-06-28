# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad

#!/usr/bin/env python3
"""Script to validate SPDX license headers in Python files.

Usage (manual):
    python scripts/validate_license_header.py file1.py file2.py
    python scripts/validate_license_header.py --all

Usage (pre-commit):
    pre-commit passes changed files automatically.
"""

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.WARNING, format="%(message)s")
logger = logging.getLogger(__name__)

SPDX_HEADER_START = "# SPDX-License-Identifier:"

IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "build",
    "dist",
    ".egg-info",
    "htmlcov",
    ".mypy_cache",
    ".ruff_cache",
}


def has_spdx_header(content: str) -> bool:
    """Check if SPDX header exists in the first lines of the file."""
    first_lines = content.splitlines()[:10]
    return any(line.startswith(SPDX_HEADER_START) for line in first_lines)


def get_all_python_files() -> list[Path]:
    """Return all .py files in the repository."""
    python_files: list[Path] = []

    for py_file in Path(".").rglob("*.py"):
        if any(skip in py_file.parts for skip in IGNORE_DIRS):
            continue

        python_files.append(py_file)

    return sorted(python_files)


def validate_files(file_paths: list[Path]) -> bool:
    """Validate the given files.

    Returns:
        True if all files have SPDX header.
    """
    missing_header: list[Path] = []

    for path in file_paths:
        if not path.exists():
            continue

        try:
            content = path.read_text(encoding="utf-8")

            if not has_spdx_header(content):
                missing_header.append(path)

        except Exception as exc:
            logger.error(f"Error checking {path}: {exc}")
            missing_header.append(path)

    if not missing_header:
        return True

    print("ERROR: The following files are missing SPDX header:\n")

    for path in missing_header:
        print(f"  - {path}")

    print(
        "\nRun:\n"
        "    python scripts/add_license_header.py\n\n"
        "Then:\n"
        "    git add <files>\n"
        "    git commit\n"
    )

    return False


def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(description="Validate SPDX headers in Python files.")

    parser.add_argument(
        "--all",
        action="store_true",
        help="Check all Python files in the repository.",
    )

    parser.add_argument(
        "files",
        nargs="*",
        help="Files passed by pre-commit.",
    )

    args = parser.parse_args()

    if args.all:
        python_files = get_all_python_files()
    else:
        python_files = [Path(file) for file in args.files if file.endswith(".py")]

    if not python_files:
        sys.exit(0)

    success = validate_files(python_files)

    if success:
        print("All files have SPDX header.")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
