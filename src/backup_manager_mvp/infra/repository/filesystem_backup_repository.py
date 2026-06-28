# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

"""Repositorio concreto de backups via filesystem local."""

import shutil
from collections.abc import Callable
from pathlib import Path

from backup_manager_mvp.core.ports.backup_repository import BackupRepositoryPort
from backup_manager_mvp.utils.paths import BACKUPS_DIR


class FileSystemBackupRepository(BackupRepositoryPort):
    """Implementacao concreta da porta de backup usando pathlib/shutil."""

    def get_backup_base_path(self) -> Path:
        return BACKUPS_DIR

    def ensure_directory(self, path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)

    def path_exists(self, path: Path) -> bool:
        return path.exists()

    def delete_tree(self, path: Path) -> None:
        shutil.rmtree(path)

    def copy_tree(self, source: Path, destination: Path, *, dirs_exist_ok: bool = False) -> None:
        shutil.copytree(source, destination, dirs_exist_ok=dirs_exist_ok)

    def copy_tree_with_progress(
        self,
        source: Path,
        destination: Path,
        progress_callback: Callable[[int, int], None] | None = None,
        *,
        dirs_exist_ok: bool = False,
    ) -> None:
        """Copia uma arvore de diretorios com rastreamento de progresso por arquivo.

        Args:
            source: Diretorio de origem
            destination: Diretorio de destino
            progress_callback: Callback chamado com (current, total) a cada arquivo copiado
            dirs_exist_ok: Se True, permite que o diretorio de destino ja exista
        """
        # Primeiro, contar total de arquivos
        total_files = 0
        for item in source.rglob("*"):
            if item.is_file():
                total_files += 1

        if total_files == 0:
            # Nao ha arquivos para copiar, apenas criar diretorio se necessario
            if dirs_exist_ok:
                destination.mkdir(parents=True, exist_ok=True)
            else:
                destination.mkdir(parents=True)
            return

        copied = 0

        def _copy_recursive(src: Path, dst: Path) -> None:
            nonlocal copied
            for item in src.iterdir():
                if item.is_dir():
                    new_dst = dst / item.name
                    new_dst.mkdir(exist_ok=True)
                    _copy_recursive(item, new_dst)
                else:
                    shutil.copy2(item, dst / item.name)
                    copied += 1
                    if progress_callback:
                        progress_callback(copied, total_files)

        if dirs_exist_ok:
            destination.mkdir(parents=True, exist_ok=True)
        else:
            destination.mkdir(parents=True)

        _copy_recursive(source, destination)

    def list_directory(self, path: Path) -> list[Path]:
        return list(path.iterdir())

    def is_directory(self, path: Path) -> bool:
        return path.is_dir()

    def delete_file(self, path: Path) -> None:
        path.unlink()

    def copy_file(self, source: Path, destination: Path) -> None:
        shutil.copy2(source, destination)

    def read_tree_stats(self, root: Path) -> tuple[int, int, int]:
        total_files = 0
        total_dirs = 0
        total_size = 0

        for item in root.rglob("*"):
            if item.is_dir():
                total_dirs += 1
            else:
                total_files += 1
                total_size += item.stat().st_size

        return total_files, total_dirs, total_size

    def read_top_level_items(self, root: Path) -> list[dict[str, int | str]]:
        items: list[dict[str, int | str]] = []

        for item in root.iterdir():
            if item.is_dir():
                item_size = sum(f.stat().st_size for f in item.rglob("*") if f.is_file())
                items.append({"name": item.name, "type": "dir", "size": item_size})
            else:
                items.append({"name": item.name, "type": "file", "size": item.stat().st_size})

        items.sort(key=lambda x: (x["type"] != "dir", x["name"]))
        return items
