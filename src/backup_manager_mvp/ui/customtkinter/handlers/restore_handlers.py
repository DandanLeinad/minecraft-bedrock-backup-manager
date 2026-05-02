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

"""Handlers para eventos de restauração."""

import logging

from backup_manager_mvp.core.models.backup_model import BackupModel
from backup_manager_mvp.core.models.world_model import WorldModel

logger = logging.getLogger(__name__)


def on_restore_backup(backup: BackupModel, world: WorldModel, callback) -> None:
    """Handler para restaurar backup.

    Args:
        backup: Backup a restaurar
        world: Mundo de destino
        callback: Callback para executar restauração
    """
    logger.debug(f"Confirmando restauração de {backup.name}")
    if callback:
        callback(backup, world)


def on_cancel_restore(backups: list[BackupModel], world: WorldModel, callback) -> None:
    """Handler para cancelar restauração.

    Args:
        backups: Lista de backups para recarregar
        world: Mundo atual
        callback: Callback para voltar aos detalhes
    """
    logger.debug("Cancelou restauração - voltando aos backups")
    if callback:
        callback(world, backups)
