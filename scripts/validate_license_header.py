# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad

#!/usr/bin/env python3
"""Script para validar headers de licença SPDX em arquivos Python.

Uso (manual):
    python scripts/validate_license_header.py

Uso (pre-commit hook):
    Chamado automaticamente por .git/hooks/pre-commit
"""

import logging
import subprocess
import sys
from pathlib import Path

logging.basicConfig(level=logging.WARNING, format="%(message)s")
logger = logging.getLogger(__name__)

SPDX_HEADER_START = "# SPDX-License-Identifier:"


def has_spdx_header(content: str) -> bool:
    """Verifica se arquivo tem header SPDX."""
    return content.lstrip().startswith(SPDX_HEADER_START)


def get_staged_python_files() -> list[str]:
    """Retorna lista de arquivos .py staged para commit."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
            check=False,
        )
        files = result.stdout.strip().split("\n")
        return [f for f in files if f.endswith(".py") and f]
    except Exception as e:
        logger.error(f"Erro ao obter arquivos staged: {e}")
        return []


def validate_files(file_paths: list[str]) -> bool:
    """Valida headers de licença SPDX em arquivos.

    Returns:
        True se todos têm header SPDX, False caso contrário
    """
    missing_header = []

    for file_path in file_paths:
        path = Path(file_path)

        if not path.exists():
            continue

        try:
            content = path.read_text(encoding="utf-8")

            if not has_spdx_header(content):
                missing_header.append(path)

        except Exception as e:
            logger.error(f"Erro ao verificar {file_path}: {e}")

    if missing_header:
        print("[-] ERRO: Arquivos sem header de licença SPDX:")
        print()
        for path in missing_header:
            print(f"   • {path}")
        print()
        print("[!] Execute para adicionar headers automaticamente:")
        print("   python scripts/add_license_header.py")
        print()
        print("[*] Depois execute: git add [arquivos] && git commit")
        print()
        return False

    return True


def main():
    """Função principal - validar headers em staged files."""
    staged_files = get_staged_python_files()

    if not staged_files:
        # Nenhum arquivo staged
        sys.exit(0)

    print(f"[*] Verificando {len(staged_files)} arquivo(s) .py...")

    if validate_files(staged_files):
        print("[+] Todos os arquivos têm header de licença SPDX!")


if __name__ == "__main__":
    main()
