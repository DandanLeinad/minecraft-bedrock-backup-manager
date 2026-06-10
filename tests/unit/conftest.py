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

from collections.abc import Callable
from pathlib import Path
from typing import Any, TypedDict

import pytest


class WorldModelData(TypedDict):
    folder_name: str
    levelname: str
    world_icon_path: Path
    path: Path
    account_id: str
    version: list[int]


@pytest.fixture
def valid_world_model_data() -> WorldModelData:
    return {
        "folder_name": "6LknJ3qXcJo=",
        "levelname": "My World",
        "path": Path(
            "C:/Users/usuario/AppData/Roaming/Minecraft Bedrock/Users/9603359306719601750/games/com.mojang/minecraftWorlds/6LknJ3qXcJo="
        ),
        "world_icon_path": Path(
            "C:/Users/usuario/AppData/Roaming/Minecraft Bedrock/Users/9603359306719601750/games/com.mojang/minecraftWorlds/6LknJ3qXcJo=/world_icon.jpeg"
        ),
        "account_id": "9603359306719601750",
        "version": [1, 26, 12, 2, 0],
    }


@pytest.fixture
def make_invalid_world_model_data(
    valid_world_model_data: WorldModelData,
) -> Callable[[str, Any], WorldModelData]:
    def _create(field_name: str, invalid_value):
        data = valid_world_model_data.copy()
        data[field_name] = invalid_value
        return data

    return _create
