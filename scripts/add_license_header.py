# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad

#!/usr/bin/env python3
"""Script para adicionar header de licença SPDX em arquivos Python.

Uso:
    python scripts/add_license_header.py                    # Encontra e atualiza todos .py
    python scripts/add_license_header.py src/backup_manager_mvp  # Um diretório específico
    python scripts/add_license_header.py file.py            # Um arquivo específico
"""

import logging
import re
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Novo cabeçalho SPDX (formato moderno)
SPDX_LICENSE_HEADER = """# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad"""

# Padrão para detectar o antigo header completo AGPL
OLD_AGPL_HEADER_PATTERN = re.compile(
    r"# minecraft-bedrock-backup-manager\s*\n"
    r"# Copyright \(C\) 2026\s+DandanLeinad\s*\n"
    r"(?:#.*\n)*?"
    r"# You should have received a copy of the GNU Affero General Public License\s*\n"
    r"# along with this program\. If not, see <https://www\.gnu\.org/licenses/>",
    re.MULTILINE,
)


def has_spdx_header(content: str) -> bool:
    """Verifica se arquivo já tem header SPDX."""
    return content.lstrip().startswith("# SPDX-License-Identifier:")


def has_old_agpl_header(content: str) -> bool:
    """Verifica se arquivo tem o antigo header AGPL completo."""
    return bool(OLD_AGPL_HEADER_PATTERN.search(content))


def add_license_header(file_path: Path) -> bool:
    """Adiciona header de licença SPDX em arquivo.

    Returns:
        True se foi adicionado/substituído, False se já tinha header SPDX
    """
    try:
        content = file_path.read_text(encoding="utf-8")

        # Se já tem header SPDX, não faz nada
        if has_spdx_header(content):
            logger.info(f"[+] {file_path} - já tem header SPDX")
            return False

        # Se tem o antigo header AGPL, substitui pelo novo SPDX
        if has_old_agpl_header(content):
            new_content = OLD_AGPL_HEADER_PATTERN.sub(SPDX_LICENSE_HEADER, content, count=1)
            file_path.write_text(new_content, encoding="utf-8")
            logger.info(f"[~] {file_path} - header AGPL antigo substituído por SPDX")
            return True

        # Adicionar novo header SPDX + linha vazia + conteúdo original
        new_content = f"{SPDX_LICENSE_HEADER}\n\n{content}"
        file_path.write_text(new_content, encoding="utf-8")
        logger.info(f"[+] {file_path} - header SPDX adicionado")
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
    target = sys.argv[1] if len(sys.argv) > 1 else "."

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
        f"\n[+] Resumo: {added} arquivo(s) atualizado(s), {len(python_files) - added} já tinham header SPDX"
    )


if __name__ == "__main__":
    main()
