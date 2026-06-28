# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

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
