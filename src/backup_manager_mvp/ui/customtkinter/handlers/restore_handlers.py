# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

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
