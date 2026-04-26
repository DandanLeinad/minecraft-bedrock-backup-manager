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

"""Repositorio concreto de backups via filesystem local."""

import shutil
from pathlib import Path

from backup_manager_mvp.utils.paths import BACKUPS_DIR


class FileSystemBackupRepository:
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
