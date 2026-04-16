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

"""Handlers para eventos de mundo."""

import logging

from backup_manager_mvp.models.world_model import WorldModel

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
