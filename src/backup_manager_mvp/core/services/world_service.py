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
        """Retorna o caminho base para os mundos Minecraft Bedrock.

        Returns:
            Path: Caminho para C:\\Users\\{usuario}\\AppData\\Roaming\\Minecraft Bedrock\\Users\\

        Notes:
            Este é o caminho padrão após a atualização 1.21.120 do Minecraft Bedrock.
        """
        return self.repository.get_worlds_base_path()

    def get_uwp_store_path(self) -> Path:
        """Retorna o caminho para mundos do UWP Store (Windows 10 Microsoft Store).

        Returns:
            Path: Caminho para C:\\Users\\{usuario}\\AppData\\Local\\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang\\minecraftWorlds

        Notes:
            Esta é a localização de mundos para a versão UWP do Minecraft no Windows 10.
        """
        return self.repository.get_uwp_store_path()

    def get_shared_path(self) -> Path:
        """Retorna o caminho para mundos compartilhados (Shared).

        Returns:
            Path: Caminho para C:\\Users\\{usuario}\\AppData\\Roaming\\Minecraft Bedrock\\Users\\Shared\\games\\com.mojang\\minecraftWorlds

        Notes:
            Esta é a localização de mundos em modo compartilhado (menos comum).
        """
        return self.repository.get_shared_path(self.get_worlds_base_path())

    def list_account_ids(self) -> list[str]:
        """Lista todos os account_ids presentes no sistema.

        Returns:
            list[str]: Lista contendo os IDs das contas Microsoft encontradas.
                Retorna lista vazia se nenhuma conta for encontrada.

        Notes:
            Cada account_id é uma pasta dentro do diretório base.
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
        """Helper privado: Lista mundos de um diretório específico com account_id dado.

        Args:
            worlds_dir (Path): Caminho para a pasta minecraftWorlds.
            account_id (str): ID da conta a associar aos mundos encontrados.

        Returns:
            list[WorldModel]: Lista de mundos encontrados neste diretório.
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
        """Lista todos os mundos de todas as sources (contas normais, UWP, Shared).

        Returns:
            list[WorldModel]: Lista contendo WorldModel para cada mundo encontrado.
                Retorna lista vazia se nenhum mundo for encontrado.

        Notes:
            Percorre 3 sources:
            1. Contas normais: base_path/account_id/games/com.mojang/minecraftWorlds/
            2. UWP Store: %LocalAppData%/Packages/Microsoft.MinecraftUWP_8wekyb3d8bbwe/.../minecraftWorlds/
            3. Shared: base_path/../Shared/games/com.mojang/minecraftWorlds/

            Cada pasta recebe validação e conversão em WorldModel.
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
        """Lê o levelname de um mundo a partir do arquivo levelname.txt.

        Args:
            world_path (Path): Caminho da pasta do mundo.

        Returns:
            str: Nome do mundo (levelname).

        Raises:
            FileNotFoundError: Se levelname.txt não existir no diretório.
            ValueError: Se o arquivo estiver vazio ou contiver apenas whitespace.
        """
        levelname_file = world_path / "levelname.txt"

        if not self.repository.path_exists(levelname_file):
            raise FileNotFoundError(f"levelname.txt não encontrado em {world_path}")

        try:
            levelname = self.repository.read_text_file(levelname_file).strip()
            if not levelname:
                raise ValueError("levelname.txt está vazio ou contém apenas whitespace")
            return levelname
        except UnicodeDecodeError as e:
            raise ValueError(f"Erro ao decodificar levelname.txt: {e}")

    def get_world_metadata(self, world: WorldModel, backup_service=None) -> dict[str, str]:
        """Calcula metadados do mundo: tamanho, quantidade de backups, último backup.

        Args:
            world: WorldModel para obter metadados
            backup_service: BackupService opcional para calcular informações de backups

        Returns:
            Dict com chaves: 'size', 'backups_count', 'last_backup'
        """
        metadata = {"size": "N/A", "backups_count": "0", "last_backup": "Nunca"}

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

            # === BACKUPS DO MUNDO ===
            if backup_service:
                try:
                    backups = backup_service.list_backups(world)
                    metadata["backups_count"] = str(len(backups))
                    logger.debug(f"Backups encontrados para {world.levelname}: {len(backups)}")

                    if backups:
                        # Último backup (mais recente)
                        last_backup = max(backups, key=lambda b: b.created_at)
                        time_diff = datetime.now() - last_backup.created_at

                        # Formatar tempo relativo
                        if time_diff.total_seconds() < 60:
                            metadata["last_backup"] = "há segundos"
                        elif time_diff.total_seconds() < 3600:
                            minutes = int(time_diff.total_seconds() / 60)
                            metadata["last_backup"] = f"há {minutes}m"
                        elif time_diff.total_seconds() < 86400:
                            hours = int(time_diff.total_seconds() / 3600)
                            metadata["last_backup"] = f"há {hours}h"
                        else:
                            days = int(time_diff.total_seconds() / 86400)
                            metadata["last_backup"] = f"há {days}d"
                        logger.debug(f"Último backup: {metadata['last_backup']}")
                except Exception as e:
                    logger.debug(f"Erro ao calcular metadados de backups: {e}")

        except Exception as e:
            logger.debug(f"Erro ao calcular metadados do mundo: {e}")

        return metadata
