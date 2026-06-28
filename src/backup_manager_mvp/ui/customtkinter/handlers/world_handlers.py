# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

"""Handlers para eventos de mundo."""

import logging

from backup_manager_mvp.core.models.world_model import WorldModel

logger = logging.getLogger(__name__)


def on_world_selected(world: WorldModel, callback) -> None:
    """Handler para seleção de mundo.

    Args:
        world: Mundo selecionado
        callback: Callback para executar após seleção
    """
    logger.debug(f"Mundo selecionado: {world.levelname}")
    if callback:
        callback(world)
