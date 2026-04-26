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

"""Porta de persistencia para operacoes de backup."""

from pathlib import Path
from typing import Protocol


class BackupRepositoryPort(Protocol):
    """Contrato para acesso a sistema de arquivos de backups."""

    def get_backup_base_path(self) -> Path:
        """Retorna o diretorio base dos backups."""

    def ensure_directory(self, path: Path) -> None:
        """Garante que um diretorio exista."""

    def path_exists(self, path: Path) -> bool:
        """Retorna se o caminho existe."""

    def delete_tree(self, path: Path) -> None:
        """Remove uma arvore de diretorios."""

    def copy_tree(self, source: Path, destination: Path, *, dirs_exist_ok: bool = False) -> None:
        """Copia uma arvore de diretorios."""

    def list_directory(self, path: Path) -> list[Path]:
        """Lista itens de um diretorio."""

    def is_directory(self, path: Path) -> bool:
        """Retorna se o caminho e um diretorio."""

    def delete_file(self, path: Path) -> None:
        """Remove arquivo."""

    def copy_file(self, source: Path, destination: Path) -> None:
        """Copia arquivo preservando metadados."""

    def read_tree_stats(self, root: Path) -> tuple[int, int, int]:
        """Retorna (total_files, total_dirs, total_size)."""

    def read_top_level_items(self, root: Path) -> list[dict[str, int | str]]:
        """Retorna itens de nivel 1 no formato esperado pela UI."""
