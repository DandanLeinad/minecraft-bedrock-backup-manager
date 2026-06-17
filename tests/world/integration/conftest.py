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

"""Fixtures for integration tests with real filesystem."""

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from backup_manager_mvp.core.models.world_model import WorldModel
from backup_manager_mvp.infra.repository import (
    FileSystemBackupRepository,
    FileSystemWorldRepository,
)


class TestFileSystemWorldRepository(FileSystemWorldRepository):
    """Test repository that uses a temporary directory instead of the real one."""

    def __init__(self, base_path: Path):
        self._test_base_path = base_path
        # Do not call super().__init__() to avoid initializing the real pathlib

    def get_worlds_base_path(self) -> Path:
        return self._test_base_path

    def get_uwp_store_path(self) -> Path:
        return self._test_base_path / "uwp_store"

    def get_shared_path(self, worlds_base_path: Path) -> Path:
        return self._test_base_path / "shared"

    # Inherit methods from parent - FileSystemWorldRepository already implements:
    # path_exists, list_directory, is_directory, read_text_file, calculate_total_size
    # which use native pathlib.Path methods


@pytest.fixture
def temp_dir() -> Generator[Path]:
    """Creates a temporary directory that is cleaned up after the test."""
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


@pytest.fixture
def test_worlds_base_path(temp_dir: Path) -> Path:
    """Creates base directory for test worlds."""
    base = temp_dir / "minecraft_worlds"
    base.mkdir(parents=True, exist_ok=True)
    return base


@pytest.fixture
def fs_world_repo(test_worlds_base_path: Path):
    """Returns world repository configured for tests."""
    return TestFileSystemWorldRepository(test_worlds_base_path)


@pytest.fixture
def fs_backup_repo() -> FileSystemBackupRepository:
    """Returns backup repository with real filesystem."""
    return FileSystemBackupRepository()


@pytest.fixture
def sample_world_dir(test_worlds_base_path: Path) -> Path:
    """Creates a valid world directory for tests in the correct base path.

    Creates the structure expected by WorldService:
    test_worlds_base_path / account_id / games / com.mojang / minecraftWorlds / world_folder
    """
    # Create the directory structure expected by WorldService
    account_id = "test_account_123"
    world_dir = (
        test_worlds_base_path
        / account_id
        / "games"
        / "com.mojang"
        / "minecraftWorlds"
        / "6LknJ3qXcJo="
    )
    world_dir.mkdir(parents=True, exist_ok=True)

    # Create levelname.txt
    (world_dir / "levelname.txt").write_text("Test World", encoding="utf-8")

    # Create level.dat (dummy file)
    (world_dir / "level.dat").write_bytes(b"dummy level data")

    # Create some files and subdirectories to simulate a real world
    (world_dir / "db").mkdir()
    (world_dir / "db" / "leveldb").write_bytes(b"dummy db data")

    (world_dir / "region").mkdir()
    (world_dir / "region" / "r.0.0.mca").write_bytes(b"dummy region data")

    return world_dir


@pytest.fixture
def sample_world_model(sample_world_dir: Path) -> WorldModel:
    """Creates a valid WorldModel pointing to the test directory."""
    from backup_manager_mvp.core.models.world_model import WorldModel

    return WorldModel(
        folder_name=sample_world_dir.name,
        levelname="Test World",
        world_icon_path=sample_world_dir / "world_icon.jpeg",
        path=sample_world_dir,
        account_id="test_account_123",
        version=[1, 26, 12, 2, 0],
    )


@pytest.fixture
def backup_base_dir(temp_dir: Path) -> Path:
    """Creates base directory for backups."""
    backup_dir = temp_dir / "backups"
    backup_dir.mkdir()
    return backup_dir


@pytest.fixture
def fs_backup_repo_with_base(backup_base_dir: Path) -> FileSystemBackupRepository:
    """Returns backup repository configured with custom base dir."""
    import backup_manager_mvp.utils.paths as paths_module

    # Temporary monkey patch of BACKUPS_DIR
    original_backups_dir = paths_module.BACKUPS_DIR
    paths_module.BACKUPS_DIR = backup_base_dir

    repo = FileSystemBackupRepository()

    # Restore after use
    yield repo

    paths_module.BACKUPS_DIR = original_backups_dir
