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
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from backup_manager_mvp.core.models.backup_model import BackupModel
from backup_manager_mvp.core.models.progress_model import ProgressModel
from backup_manager_mvp.core.models.world_model import WorldModel
from backup_manager_mvp.core.ports.backup_repository import BackupRepositoryPort

logger = logging.getLogger(__name__)


class BackupService:
    """Serviço para operações de backup e restauração de mundos Minecraft Bedrock."""

    def __init__(self, repository: BackupRepositoryPort):
        """Inicializa o serviço com uma implementação de repositório de backup."""
        self.repository = repository

    def get_backup_base_path(self) -> Path:
        """Retorna o caminho base para armazenar backups.

        Returns:
            Path: Caminho para C:\\Users\\{usuario}\\Documents\\MinecraftBackups\\backups\\

        Notes:
            Este é o local fixo onde todos os backups são armazenados.
            Não é configurável no MVP.
        """
        return self.repository.get_backup_base_path()

    def create_backup(
        self,
        world: WorldModel,
        progress_callback: Callable[[ProgressModel], None] | None = None,
    ) -> BackupModel:
        """Cria um backup de um mundo com rastreamento de progresso opcional.

        Args:
            world (WorldModel): Modelo do mundo a ser feito backup.
            progress_callback: Função chamada com ProgressModel durante a cópia.
                              Assinatura: callback(progress: ProgressModel) -> None
                              Opcional, pode ser None.

        Returns:
            BackupModel: Modelo contendo informações sobre o backup criado.

        Notes:
            - A pasta de backup usa folder_name (UUID Bedrock) para persistir
              mesmo que o usuário renomeie o mundo
            - Estrutura: backup_base / {folder_name} / {YYYY-MM-DD_HH-MM-SS}
            - O conteúdo completo da pasta do mundo é copiado
            - Se a pasta de backup não existir, é criada automaticamente
            - Progress callback é chamado durante a cópia de arquivos
        """
        # Gerar timestamp para o backup
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

        # Determinar o caminho do backup (usando folder_name, não levelname)
        backup_base = self.get_backup_base_path()
        world_backup_dir = backup_base / world.folder_name
        backup_path = world_backup_dir / timestamp

        # Criar diretórios se não existirem
        self.repository.ensure_directory(world_backup_dir)

        # Copiar a pasta do mundo para o backup
        # Primeiro, removemos a pasta de destino se ela existir (normalmente não existe)
        # Limpar destino se por algum motivo já existir (evita erro no copytree)
        if self.repository.path_exists(backup_path):
            self.repository.delete_tree(backup_path)

        try:
            # Reportar início da operação
            if progress_callback:
                progress_callback(ProgressModel(current=0, total=1, stage="Preparando backup..."))

            # Copiar todo o conteúdo do mundo
            # TODO: Implementar cópia com rastreamento de arquivos individuais
            self.repository.copy_tree(world.path, backup_path, dirs_exist_ok=True)

            # Reportar conclusão
            if progress_callback:
                progress_callback(
                    ProgressModel(
                        current=1,
                        total=1,
                        stage=f"Backup concluído: {backup_path.name}",
                    )
                )
        except Exception as e:
            # Se falhar, tentar remover a pasta criada
            if self.repository.path_exists(backup_path):
                self.repository.delete_tree(backup_path)
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

        if not self.repository.path_exists(world_backup_dir):
            return []

        backups = []

        try:
            for backup_folder in self.repository.list_directory(world_backup_dir):
                if not self.repository.is_directory(backup_folder):
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
                except ValueError, OSError:
                    # Ignorar pastas com nomes inválidos
                    continue

        except OSError, PermissionError:
            return []

        # Ordenar do mais recente ao mais antigo
        backups.sort(key=lambda b: b.created_at, reverse=True)

        return backups

    def restore_backup(
        self,
        backup: BackupModel,
        world: WorldModel,
        progress_callback: Callable[[ProgressModel], None] | None = None,
    ) -> None:
        """Restaura um mundo a partir de um backup com rastreamento de progresso opcional.

        Args:
            backup (BackupModel): Backup a ser restaurado.
            world (WorldModel): Mundo que será substituído.
            progress_callback: Função chamada com ProgressModel durante a restauração.
                              Assinatura: callback(progress: ProgressModel) -> None
                              Opcional, pode ser None.

        Raises:
            FileNotFoundError: Se o backup não existir.
            RuntimeError: Se ocorrer erro durante a restauração.

        Notes:
            - O conteúdo atual do mundo é substituído
            - O backup original NÃO é alterado
            - Esta é uma operação destrutiva no mundo atual
        """
        if not self.repository.path_exists(backup.backup_path):
            raise FileNotFoundError(f"Backup não encontrado: {backup.backup_path}")

        if not self.repository.path_exists(world.path):
            raise FileNotFoundError(f"Mundo não encontrado: {world.path}")

        try:
            # Reportar início da operação
            if progress_callback:
                progress_callback(
                    ProgressModel(current=0, total=1, stage="Limpando mundo atual...")
                )

            # Remover conteúdo atual da pasta do mundo (mantendo a pasta)
            for item in self.repository.list_directory(world.path):
                if self.repository.is_directory(item):
                    self.repository.delete_tree(item)
                else:
                    self.repository.delete_file(item)

            # Reportar fase de cópia
            if progress_callback:
                progress_callback(
                    ProgressModel(current=0, total=1, stage="Restaurando arquivos do backup...")
                )

            # Copiar conteúdo do backup para o mundo
            for item in self.repository.list_directory(backup.backup_path):
                if self.repository.is_directory(item):
                    self.repository.copy_tree(item, world.path / item.name)
                else:
                    self.repository.copy_file(item, world.path / item.name)

            # Reportar conclusão
            if progress_callback:
                progress_callback(ProgressModel(current=1, total=1, stage="Restauração concluída!"))

        except Exception as e:
            raise RuntimeError(f"Erro ao restaurar backup: {e}")

    def get_backup_preview_info(self, backup: BackupModel) -> dict:
        """Retorna informações sobre o conteúdo do backup para preview.

        Args:
            backup (BackupModel): Backup a ser analisado.

        Returns:
            dict: Dicionário com estrutura do backup:
                {
                    "total_files": int,           # Total de arquivos (recursivo)
                    "total_dirs": int,             # Total de diretórios (recursivo)
                    "total_size": int,             # Tamanho em bytes
                    "top_level_items": list,       # Itens de nível 1
                    "error": str|None              # Erro se houver
                }

        Notes:
            - top_level_items: lista de {"name": str, "type": "file"|"dir", "size": int}
            - Se um arquivo for muito grande, mostra "..." no final da lista
            - Útil para FF_RESTORE_PREVIEW (mostrar conteúdo antes de restaurar)
        """
        try:
            if not self.repository.path_exists(backup.backup_path):
                return {
                    "total_files": 0,
                    "total_dirs": 0,
                    "total_size": 0,
                    "top_level_items": [],
                    "error": f"Backup não encontrado: {backup.backup_path}",
                }

            total_files, total_dirs, total_size = self.repository.read_tree_stats(
                backup.backup_path
            )
            top_level_items = self.repository.read_top_level_items(backup.backup_path)

            # Limitar a 20 itens para não poluir a UI
            if len(top_level_items) > 20:
                top_level_items = top_level_items[:20]
                top_level_items.append({"name": "... e mais itens", "type": "ellipsis", "size": 0})

            return {
                "total_files": total_files,
                "total_dirs": total_dirs,
                "total_size": total_size,
                "top_level_items": top_level_items,
                "error": None,
            }

        except Exception as e:
            logger.error(f"Erro ao analisar preview do backup: {e}", exc_info=True)
            return {
                "total_files": 0,
                "total_dirs": 0,
                "total_size": 0,
                "top_level_items": [],
                "error": f"Erro ao ler backup: {e!s}",
            }
