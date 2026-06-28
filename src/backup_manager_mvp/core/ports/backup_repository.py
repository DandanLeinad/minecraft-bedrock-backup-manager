# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

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
