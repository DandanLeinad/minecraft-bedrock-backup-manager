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
"""Script para adicionar header de licença AGPL em arquivos Python.

Uso:
    python scripts/add_license_header.py                    # Encontra e atualiza todos .py
    python scripts/add_license_header.py src/backup_manager_mvp  # Um diretório específico
    python scripts/add_license_header.py file.py            # Um arquivo específico
"""

import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

LICENSE_HEADER = """# minecraft-bedrock-backup-manager
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
# along with this program. If not, see <https://www.gnu.org/licenses/>."""


def has_license_header(content: str) -> bool:
    """Verifica se arquivo já tem header de licença."""
    return content.strip().startswith("# minecraft-bedrock-backup-manager")


def add_license_header(file_path: Path) -> bool:
    """Adiciona header de licença em arquivo.

    Returns:
        True se foi adicionado, False se já tinha
    """
    try:
        content = file_path.read_text(encoding="utf-8")

        if has_license_header(content):
            logger.info(f"[+] {file_path} - já tem header")
            return False

        # Adicionar header + linha vazia + conteúdo original
        new_content = f"{LICENSE_HEADER}\n\n{content}"
        file_path.write_text(new_content, encoding="utf-8")
        logger.info(f"[+] {file_path} - header adicionado")
        return True

    except Exception as e:
        logger.error(f"[-] {file_path} - erro: {e}")
        return False


def find_python_files(path: Path | str) -> list[Path]:
    """Encontra todos os arquivos .py recursivamente."""
    path = Path(path)

    if path.is_file():
        return [path] if path.suffix == ".py" else []

    # Ignorar diretórios
    ignore_dirs = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".pytest_cache",
        "build",
        "dist",
        ".egg-info",
        "htmlcov",
    }

    python_files = []
    for py_file in path.rglob("*.py"):
        # Verificar se está em diretório ignorado
        if not any(skip in py_file.parts for skip in ignore_dirs):
            python_files.append(py_file)

    return sorted(python_files)


def main():
    """Função principal."""
    # Determinar caminho: argumento ou raiz do projeto
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = "."

    target_path = Path(target)

    if not target_path.exists():
        logger.error(f"Caminho não existe: {target}")
        sys.exit(1)

    logger.info(f"[*] Procurando arquivos .py em: {target_path.resolve()}")
    python_files = find_python_files(target_path)

    if not python_files:
        logger.warning("Nenhum arquivo .py encontrado")
        sys.exit(0)

    logger.info(f"[*] Encontrados {len(python_files)} arquivo(s) .py\n")

    # Adicionar headers
    added = 0
    for file_path in python_files:
        if add_license_header(file_path):
            added += 1

    logger.info(
        f"\n[+] Resumo: {added} arquivo(s) atualizado(s), {len(python_files) - added} já tinham header"
    )


if __name__ == "__main__":
    main()
