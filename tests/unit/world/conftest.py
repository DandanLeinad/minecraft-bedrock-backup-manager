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

from pathlib import Path

import pytest

from backup_manager_mvp.core.models.world_model import WorldModel
from backup_manager_mvp.core.services.world_service import WorldService
from backup_manager_mvp.infra.repository import FileSystemWorldRepository


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
        path=world_path,
        account_id="test_account",
        version=[1, 26, 12, 2, 0],
    )
