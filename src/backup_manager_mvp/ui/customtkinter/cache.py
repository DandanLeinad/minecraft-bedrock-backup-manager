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

"""Cache em memória para backups com invalidação por TTL.

Responsável por:
- Armazenar lista de backups em cache
- Validar TTL (Time To Live)
- Invalidar cache específico ou global
"""

import logging
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backup_manager_mvp.models.backup_model import BackupModel

logger = logging.getLogger(__name__)


class BackupCache:
    """Cache simples para backups com invalidação por timestamp."""

    def __init__(self, ttl_seconds: int = 60):
        """Inicializa cache com TTL em segundos.

        Args:
            ttl_seconds: Tempo de vida do cache em segundos (padrão: 60s)
        """
        self.ttl_seconds = ttl_seconds
        self._cache: dict[str, tuple[list[BackupModel], float]] = {}

    def get(self, world_folder_name: str) -> list[BackupModel] | None:
        """Retorna backups do cache se válido, None caso contrário.

        Args:
            world_folder_name: Nome da pasta do mundo

        Returns:
            Lista de backups se existir e ser válido, None caso contrário
        """
        if world_folder_name not in self._cache:
            return None

        backups, timestamp = self._cache[world_folder_name]
        if datetime.now().timestamp() - timestamp > self.ttl_seconds:
            del self._cache[world_folder_name]
            return None

        logger.debug(f"Cache hit para {world_folder_name}")
        return backups

    def set(self, world_folder_name: str, backups: list[BackupModel]) -> None:
        """Armazena backups no cache com timestamp.

        Args:
            world_folder_name: Nome da pasta do mundo
            backups: Lista de backups para armazenar
        """
        self._cache[world_folder_name] = (backups, datetime.now().timestamp())
        logger.debug(f"Cache set para {world_folder_name} ({len(backups)} backups)")

    def invalidate(self, world_folder_name: str | None = None) -> None:
        """Invalida cache (específico ou completo).

        Args:
            world_folder_name: Nome da pasta específica para invalidar ou None para limpar tudo
        """
        if world_folder_name:
            self._cache.pop(world_folder_name, None)
        else:
            self._cache.clear()
