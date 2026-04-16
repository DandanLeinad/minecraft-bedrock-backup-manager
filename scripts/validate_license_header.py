# minecraft-bedrock-backup-manager
# Copyright (C) 2026  DandanLeinad
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

#!/usr/bin/env python3
"""Script para validar headers de licença em arquivos Python.

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

LICENSE_HEADER_START = "# minecraft-bedrock-backup-manager"


def has_license_header(content: str) -> bool:
    """Verifica se arquivo tem header de licença."""
    return content.strip().startswith(LICENSE_HEADER_START)


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
    """Valida headers de licença em arquivos.

    Returns:
        True se todos têm header, False caso contrário
    """
    missing_header = []

    for file_path in file_paths:
        path = Path(file_path)

        if not path.exists():
            continue

        try:
            content = path.read_text(encoding="utf-8")

            if not has_license_header(content):
                missing_header.append(path)

        except Exception as e:
            logger.error(f"Erro ao verificar {file_path}: {e}")

    if missing_header:
        print("[-] ERRO: Arquivos sem header de licença AGPL:")
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
        print("[+] Todos os arquivos têm header de licença!")
