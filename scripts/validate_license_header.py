# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad

#!/usr/bin/env python3
"""Script para validar headers de licença SPDX em arquivos Python.

Uso (manual):
    python scripts/validate_license_header.py arquivo1.py arquivo2.py
    python scripts/validate_license_header.py --all

Uso (pre-commit):
    O pre-commit passa automaticamente os arquivos alterados.
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
    """Verifica se existe um header SPDX nas primeiras linhas do arquivo."""
    first_lines = content.splitlines()[:10]
    return any(line.startswith(SPDX_HEADER_START) for line in first_lines)


def get_all_python_files() -> list[Path]:
    """Retorna todos os arquivos .py do repositório."""
    python_files: list[Path] = []

    for py_file in Path(".").rglob("*.py"):
        if any(skip in py_file.parts for skip in IGNORE_DIRS):
            continue

        python_files.append(py_file)

    return sorted(python_files)


def validate_files(file_paths: list[Path]) -> bool:
    """Valida os arquivos informados.

    Returns:
        True se todos possuem header SPDX.
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
            logger.error(f"Erro ao verificar {path}: {exc}")
            missing_header.append(path)

    if not missing_header:
        return True

    print("ERRO: Os seguintes arquivos não possuem header SPDX:\n")

    for path in missing_header:
        print(f"  • {path}")

    print(
        "\nExecute:\n"
        "    python scripts/add_license_header.py\n\n"
        "Depois:\n"
        "    git add <arquivos>\n"
        "    git commit\n"
    )

    return False


def main() -> None:
    """Função principal."""
    parser = argparse.ArgumentParser(description="Valida headers SPDX em arquivos Python.")

    parser.add_argument(
        "--all",
        action="store_true",
        help="Verifica todos os arquivos Python do repositório.",
    )

    parser.add_argument(
        "files",
        nargs="*",
        help="Arquivos recebidos pelo pre-commit.",
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
        print("Todos os arquivos possuem header SPDX.")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
