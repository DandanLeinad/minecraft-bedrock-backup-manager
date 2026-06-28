# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

"""Repositorio concreto de mundos via filesystem local."""

from pathlib import Path

from backup_manager_mvp.core.ports.world_repository import WorldRepositoryPort


class FileSystemWorldRepository(WorldRepositoryPort):
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
