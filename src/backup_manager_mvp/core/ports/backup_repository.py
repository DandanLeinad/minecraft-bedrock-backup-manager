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

from abc import ABC, abstractmethod
from collections.abc import Callable
from pathlib import Path


class BackupRepositoryPort(ABC):
    """Contrato para acesso a sistema de arquivos de backups."""

    @abstractmethod
    def get_backup_base_path(self) -> Path:
        """Retorna o diretorio base dos backups."""

    @abstractmethod
    def ensure_directory(self, path: Path) -> None:
        """Garante que um diretorio exista."""

    @abstractmethod
    def path_exists(self, path: Path) -> bool:
        """Retorna se o caminho existe."""

    @abstractmethod
    def delete_tree(self, path: Path) -> None:
        """Remove uma arvore de diretorios."""

    @abstractmethod
    def copy_tree(self, source: Path, destination: Path, *, dirs_exist_ok: bool = False) -> None:
        """Copia uma arvore de diretorios."""

    @abstractmethod
    def list_directory(self, path: Path) -> list[Path]:
        """Lista itens de um diretorio."""

    @abstractmethod
    def is_directory(self, path: Path) -> bool:
        """Retorna se o caminho e um diretorio."""

    @abstractmethod
    def delete_file(self, path: Path) -> None:
        """Remove arquivo."""

    @abstractmethod
    def copy_file(self, source: Path, destination: Path) -> None:
        """Copia arquivo preservando metadados."""

    @abstractmethod
    def read_tree_stats(self, root: Path) -> tuple[int, int, int]:
        """Retorna (total_files, total_dirs, total_size)."""

    @abstractmethod
    def read_top_level_items(self, root: Path) -> list[dict[str, int | str]]:
        """Retorna itens de nivel 1 no formato esperado pela UI."""

    @abstractmethod
    def copy_tree_with_progress(
        self,
        source: Path,
        destination: Path,
        progress_callback: Callable[[int, int], None] | None = None,
        *,
        dirs_exist_ok: bool = False,
    ) -> None:
        """Copia uma arvore de diretorios com rastreamento de progresso.

        Args:
            source: Diretorio de origem
            destination: Diretorio de destino
            progress_callback: Callback chamado com (current, total) a cada arquivo copiado
            dirs_exist_ok: Se True, permite que o diretorio de destino ja exista
        """
