# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

import logging
from datetime import datetime
from pathlib import Path

from backup_manager_mvp.core.models.world_model import WorldModel
from backup_manager_mvp.core.ports.world_repository import WorldRepositoryPort

logger = logging.getLogger(__name__)

# Constantes para account_ids especiais (sem conta Microsoft real)
ACCOUNT_UWP_STORE = "UWP-Store"  # Windows 10 Microsoft Store
ACCOUNT_SHARED = "Shared"  # Modo compartilhado


class WorldService:
    """Serviço para operações relacionadas a mundos Minecraft Bedrock."""

    def __init__(self, repository: WorldRepositoryPort):
        """Inicializa o serviço com uma implementação de repositório de mundos."""
        self.repository = repository

    def get_worlds_base_path(self) -> Path:
        """Returns the base path for Minecraft Bedrock worlds.

        Returns:
            Path: Path to C:\\Users\\{user}\\AppData\\Roaming\\Minecraft Bedrock\\Users\\

        Notes:
            This is the default path after Minecraft Bedrock update 1.21.120.
        """
        return self.repository.get_worlds_base_path()

    def get_uwp_store_path(self) -> Path:
        """Returns the path for UWP Store worlds (Windows 10 Microsoft Store).

        Returns:
            Path: Path to C:\\Users\\{user}\\AppData\\Local\\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang\\minecraftWorlds

        Notes:
            This is the location of worlds for the UWP version of Minecraft on Windows 10.
        """
        return self.repository.get_uwp_store_path()

    def get_shared_path(self) -> Path:
        """Returns the path for shared worlds (Shared).

        Returns:
            Path: Path to C:\\Users\\{user}\\AppData\\Roaming\\Minecraft Bedrock\\Users\\Shared\\games\\com.mojang\\minecraftWorlds

        Notes:
            This is the location of worlds in shared mode (less common).
        """
        return self.repository.get_shared_path(self.get_worlds_base_path())

    def list_account_ids(self) -> list[str]:
        """Lists all account_ids present in the system.

        Returns:
            list[str]: List containing Microsoft account IDs found.
                Returns empty list if no accounts are found.

        Notes:
            Each account_id is a folder inside the base directory.
        """
        base_path = self.get_worlds_base_path()

        if not self.repository.path_exists(base_path):
            return []

        account_ids = []
        try:
            for item in self.repository.list_directory(base_path):
                if self.repository.is_directory(item):
                    account_ids.append(item.name)
        except OSError, PermissionError:
            # Se não conseguir ler o diretório, retorna vazio
            return []

        return sorted(account_ids)

    def _list_worlds_from_path(self, worlds_dir: Path, account_id: str) -> list[WorldModel]:
        """Private helper: Lists worlds from a specific directory with given account_id.

        Args:
            worlds_dir (Path): Path to the minecraftWorlds folder.
            account_id (str): Account ID to associate with found worlds.

        Returns:
            list[WorldModel]: List of worlds found in this directory.
        """
        worlds = []

        if not self.repository.path_exists(worlds_dir):
            return worlds

        try:
            for world_folder in self.repository.list_directory(worlds_dir):
                if not self.repository.is_directory(world_folder):
                    continue

                # Tentar ler levelname.txt
                try:
                    levelname = self.get_world_levelname(world_folder)

                    # Tentar criar WorldModel
                    world = WorldModel(
                        folder_name=world_folder.name,
                        levelname=levelname,
                        world_icon_path=self.get_world_icon_path(world_folder),
                        path=world_folder,
                        account_id=account_id,
                        version=[1, 0, 0, 0, 0],  # Versão padrão
                    )
                    worlds.append(world)
                except FileNotFoundError, ValueError:
                    # Ignorar mundos com problemas
                    continue

        except OSError, PermissionError:
            # Se não conseguir ler o diretório, retorna o que encontrou
            pass

        return worlds

    def list_worlds(self) -> list[WorldModel]:
        """Lists all worlds from all sources (normal accounts, UWP, Shared).

        Returns:
            list[WorldModel]: List containing WorldModel for each world found.
                Returns empty list if no worlds are found.

        Notes:
            Iterates over 3 sources:
            1. Normal accounts: base_path/account_id/games/com.mojang/minecraftWorlds/
            2. UWP Store: %LocalAppData%/Packages/Microsoft.MinecraftUWP_8wekyb3d8bbwe/.../minecraftWorlds/
            3. Shared: base_path/../Shared/games/com.mojang/minecraftWorlds/

            Each folder receives validation and conversion to WorldModel.
        """
        all_worlds = []

        # Source 1: Contas normais (com UUID de conta Microsoft)
        account_ids = self.list_account_ids()
        for account_id in account_ids:
            worlds_dir = (
                self.get_worlds_base_path()
                / account_id
                / "games"
                / "com.mojang"
                / "minecraftWorlds"
            )
            all_worlds.extend(self._list_worlds_from_path(worlds_dir, account_id))

        # Source 2: UWP Store (Windows 10 Microsoft Store)
        uwp_path = self.get_uwp_store_path()
        all_worlds.extend(self._list_worlds_from_path(uwp_path, ACCOUNT_UWP_STORE))

        # Source 3: Shared
        shared_path = self.get_shared_path()
        all_worlds.extend(self._list_worlds_from_path(shared_path, ACCOUNT_SHARED))

        return all_worlds

    def get_world_levelname(self, world_path: Path) -> str:
        """Reads the levelname of a world from the levelname.txt file.

        Args:
            world_path (Path): Path to the world folder.

        Returns:
            str: World name (levelname).

        Raises:
            FileNotFoundError: If levelname.txt does not exist in the directory.
            ValueError: If the file is empty or contains only whitespace.
        """
        levelname_file = world_path / "levelname.txt"

        if not self.repository.path_exists(levelname_file):
            raise FileNotFoundError(f"levelname.txt not found in {world_path}")

        try:
            levelname = self.repository.read_text_file(levelname_file).strip()
            if not levelname:
                raise ValueError("levelname.txt is empty or contains only whitespace")
            return levelname
        except UnicodeDecodeError as e:
            raise ValueError(f"Error decoding levelname.txt: {e}")

    def get_world_icon_path(self, world_path: Path) -> Path:
        """Gets the path to the world image (world_icon.jpeg).

        Args:
            world_path (Path): Path to the world folder.

        Returns:
            Path: Path to the world image.
        """
        return world_path / "world_icon.jpeg"

    def get_world_metadata(self, world: WorldModel, backup_service=None) -> dict[str, str]:
        """Calculates world metadata: size, backup count, last backup.

        Args:
            world: WorldModel to get metadata for
            backup_service: Optional BackupService to calculate backup info

        Returns:
            Dict with keys: 'size', 'backups_count', 'last_backup'
        """
        metadata = {"size": "N/A", "backups_count": "0", "last_backup": "Never"}

        try:
            # === TAMANHO DO MUNDO ===
            if self.repository.path_exists(world.path):
                total_size = self.repository.calculate_total_size(world.path)
                if total_size < 1024:
                    metadata["size"] = f"{total_size} B"
                elif total_size < 1024 * 1024:
                    metadata["size"] = f"{total_size / 1024:.1f} KB"
                elif total_size < 1024 * 1024 * 1024:
                    metadata["size"] = f"{total_size / (1024 * 1024):.1f} MB"
                else:
                    metadata["size"] = f"{total_size / (1024 * 1024 * 1024):.1f} GB"
                logger.debug(f"Tamanho do mundo {world.levelname}: {metadata['size']}")

            # === WORLD BACKUPS ===
            if backup_service:
                try:
                    backups = backup_service.list_backups(world)
                    metadata["backups_count"] = str(len(backups))
                    logger.debug(f"Backups found for {world.levelname}: {len(backups)}")

                    if backups:
                        # Last backup (most recent)
                        last_backup = max(backups, key=lambda b: b.created_at)
                        time_diff = datetime.now() - last_backup.created_at

                        # Format relative time
                        if time_diff.total_seconds() < 60:
                            metadata["last_backup"] = "seconds ago"
                        elif time_diff.total_seconds() < 3600:
                            minutes = int(time_diff.total_seconds() / 60)
                            metadata["last_backup"] = f"{minutes}m ago"
                        elif time_diff.total_seconds() < 86400:
                            hours = int(time_diff.total_seconds() / 3600)
                            metadata["last_backup"] = f"{hours}h ago"
                        else:
                            days = int(time_diff.total_seconds() / 86400)
                            metadata["last_backup"] = f"{days}d ago"
                        logger.debug(f"Last backup: {metadata['last_backup']}")
                except Exception as e:
                    logger.debug(f"Error calculating backup metadata: {e}")

        except Exception as e:
            logger.debug(f"Error calculating world metadata: {e}")

        return metadata
