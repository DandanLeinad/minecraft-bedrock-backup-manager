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
import shutil
from datetime import datetime
from pathlib import Path

from backup_manager_mvp.models.backup_model import BackupModel
from backup_manager_mvp.models.world_model import WorldModel
from backup_manager_mvp.utils.paths import BACKUPS_DIR

logger = logging.getLogger(__name__)


class BackupService:
    """Serviço para operações de backup e restauração de mundos Minecraft Bedrock."""

    def get_backup_base_path(self) -> Path:
        """Retorna o caminho base para armazenar backups.

        Returns:
            Path: Caminho para C:\\Users\\{usuario}\\Documents\\MinecraftBackups\\backups\\

        Notes:
            Este é o local fixo onde todos os backups são armazenados.
            Não é configurável no MVP.
        """
        return BACKUPS_DIR

    def create_backup(self, world: WorldModel) -> BackupModel:
        """Cria um backup de um mundo.

        Args:
            world (WorldModel): Modelo do mundo a ser feito backup.

        Returns:
            BackupModel: Modelo contendo informações sobre o backup criado.

        Notes:
            - A pasta de backup usa folder_name (UUID Bedrock) para persistir
              mesmo que o usuário renomeie o mundo
            - Estrutura: backup_base / {folder_name} / {YYYY-MM-DD_HH-MM-SS}
            - O conteúdo completo da pasta do mundo é copiado
            - Se a pasta de backup não existir, é criada automaticamente
        """
        # Gerar timestamp para o backup
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

        # Determinar o caminho do backup (usando folder_name, não levelname)
        backup_base = self.get_backup_base_path()
        world_backup_dir = backup_base / world.folder_name
        backup_path = world_backup_dir / timestamp

        # Criar diretórios se não existirem
        backup_path.mkdir(parents=True, exist_ok=True)

        # Copiar a pasta do mundo para o backup
        # Primeiro, removemos a pasta de destino se ela existir (normalmente não existe)
        if backup_path.exists():
            shutil.rmtree(backup_path)

        try:
            # Copiar todo o conteúdo do mundo
            shutil.copytree(world.path, backup_path, dirs_exist_ok=True)
        except Exception as e:
            # Se falhar, tentar remover a pasta criada
            if backup_path.exists():
                shutil.rmtree(backup_path)
            raise RuntimeError(f"Erro ao criar backup: {e}")

        # Criar e retornar BackupModel
        backup = BackupModel(
            world_folder_name=world.folder_name,
            world_account_id=world.account_id,
            created_at=now,
            backup_path=backup_path,
        )

        return backup

    def list_backups(self, world: WorldModel) -> list[BackupModel]:
        """Lista todos os backups de um mundo, ordenados do mais recente ao mais antigo.

        Args:
            world (WorldModel): Modelo do mundo.

        Returns:
            list[BackupModel]: Lista de backups ordenados por data (desc).
                Retorna lista vazia se nenhum backup existir.

        Notes:
            O ordenamento é feito por data de criação em ordem decrescente.
            Usa folder_name (não levelname) para encontrar backups mesmo após
            o usuário renomear o mundo.
        """
        backup_base = self.get_backup_base_path()
        world_backup_dir = backup_base / world.folder_name

        if not world_backup_dir.exists():
            return []

        backups = []

        try:
            for backup_folder in world_backup_dir.iterdir():
                if not backup_folder.is_dir():
                    continue

                # Tentar extrair timestamp do nome da pasta
                try:
                    # Esperado formato: YYYY-MM-DD_HH-MM-SS
                    timestamp_str = backup_folder.name
                    created_at = datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")

                    backup = BackupModel(
                        world_folder_name=world.folder_name,
                        world_account_id=world.account_id,
                        created_at=created_at,
                        backup_path=backup_folder,
                    )
                    backups.append(backup)
                except (ValueError, OSError):
                    # Ignorar pastas com nomes inválidos
                    continue

        except (OSError, PermissionError):
            return []

        # Ordenar do mais recente ao mais antigo
        backups.sort(key=lambda b: b.created_at, reverse=True)

        return backups

    def restore_backup(self, backup: BackupModel, world: WorldModel) -> None:
        """Restaura um mundo a partir de um backup.

        Args:
            backup (BackupModel): Backup a ser restaurado.
            world (WorldModel): Mundo que será substituído.

        Raises:
            FileNotFoundError: Se o backup não existir.
            RuntimeError: Se ocorrer erro durante a restauração.

        Notes:
            - O conteúdo atual do mundo é substituído
            - O backup original NÃO é alterado
            - Esta é uma operação destrutiva no mundo atual
        """
        if not backup.backup_path.exists():
            raise FileNotFoundError(f"Backup não encontrado: {backup.backup_path}")

        if not world.path.exists():
            raise FileNotFoundError(f"Mundo não encontrado: {world.path}")

        try:
            # Remover conteúdo atual da pasta do mundo (mantendo a pasta)
            for item in world.path.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()

            # Copiar conteúdo do backup para o mundo
            for item in backup.backup_path.iterdir():
                if item.is_dir():
                    shutil.copytree(item, world.path / item.name)
                else:
                    shutil.copy2(item, world.path / item.name)

        except Exception as e:
            raise RuntimeError(f"Erro ao restaurar backup: {e}")
