# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

from collections.abc import Callable
from pathlib import Path
from typing import Any, TypedDict

import pytest

from backup_manager_mvp.core.models.world_model import WorldModel
from backup_manager_mvp.core.services.world_service import WorldService
from backup_manager_mvp.infra.repository import FileSystemWorldRepository


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


@pytest.fixture
def world_service() -> WorldService:
    return WorldService(FileSystemWorldRepository())


@pytest.fixture
def sample_world(tmp_path: Path) -> WorldModel:
    world_path = tmp_path / "test_world"
    world_path.mkdir()
    (world_path / "levelname.txt").write_text("Meu Mundo")
    (world_path / "level.dat").write_bytes(b"\x00")

    return WorldModel(
        folder_name="6LknJ-+T-Ks=",
        levelname="Meu Mundo",
        world_icon_path=Path(
            "C:/Users/usuario/AppData/Roaming/Minecraft Bedrock/Users/9603359306719601750/games/com.mojang/minecraftWorlds/6LknJ-+T-Ks=/world_icon.jpeg"
        ),
        path=world_path,
        account_id="test_account",
        version=[1, 26, 12, 2, 0],
    )
