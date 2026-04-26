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

"""Repositorio concreto de mundos via filesystem local."""

from pathlib import Path


class FileSystemWorldRepository:
    """Implementacao concreta da porta de mundos usando pathlib."""

    def get_worlds_base_path(self) -> Path:
        return Path.home() / "AppData" / "Roaming" / "Minecraft Bedrock" / "Users"

    def get_uwp_store_path(self) -> Path:
        return (
            Path.home()
            / "AppData"
            / "Local"
            / "Packages"
            / "Microsoft.MinecraftUWP_8wekyb3d8bbwe"
            / "LocalState"
            / "games"
            / "com.mojang"
            / "minecraftWorlds"
        )

    def get_shared_path(self, worlds_base_path: Path) -> Path:
        return worlds_base_path.parent / "Shared" / "games" / "com.mojang" / "minecraftWorlds"

    def path_exists(self, path: Path) -> bool:
        return path.exists()

    def list_directory(self, path: Path) -> list[Path]:
        return list(path.iterdir())

    def is_directory(self, path: Path) -> bool:
        return path.is_dir()

    def read_text_file(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def calculate_total_size(self, path: Path) -> int:
        return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
