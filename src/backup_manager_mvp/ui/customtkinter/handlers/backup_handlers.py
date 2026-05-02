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

"""Handlers para eventos de backup."""

import logging

from backup_manager_mvp.core.models.backup_model import BackupModel
from backup_manager_mvp.core.models.world_model import WorldModel

logger = logging.getLogger(__name__)


def on_create_backup(world: WorldModel, callback) -> None:
    """Handler para criar backup.

    Args:
        world: Mundo para fazer backup
        callback: Callback para executar
    """
    logger.debug(f"Criando backup para: {world.levelname}")
    if callback:
        callback(world)


def on_backup_selected(backup: BackupModel, world: WorldModel, callback) -> None:
    """Handler para seleção de backup.

    Args:
        backup: Backup selecionado
        world: Mundo do backup
        callback: Callback para executar
    """
    logger.debug(f"Backup selecionado: {backup.name}")
    if callback:
        callback(backup, world)


def on_sync_backups(world: WorldModel, callback) -> None:
    """Handler para sincronizar backups.

    Args:
        world: Mundo a sincronizar
        callback: Callback para executar
    """
    logger.debug(f"Sincronizando backups de {world.levelname}")
    if callback:
        callback(world)
