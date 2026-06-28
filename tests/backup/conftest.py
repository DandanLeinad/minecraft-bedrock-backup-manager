# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

from datetime import datetime
from pathlib import Path

import pytest

from backup_manager_mvp.core.models.backup_model import BackupModel
from backup_manager_mvp.core.models.world_model import WorldModel
from backup_manager_mvp.core.services.backup_service import BackupService
from backup_manager_mvp.infra.repository import FileSystemBackupRepository


@pytest.fixture
def backup_service() -> BackupService:
    return BackupService(FileSystemBackupRepository())


@pytest.fixture
def sample_world(tmp_path: Path) -> WorldModel:
    world_path = tmp_path / "test_world"
    world_path.mkdir()
    return WorldModel(
        folder_name="6LknJ-+T-Ks=",
        levelname="Meu Mundo",
        world_icon_path=tmp_path / "world_icon.jpeg",
        path=world_path,
        account_id="test_account",
        version=[1, 26, 12, 2, 0],
    )


@pytest.fixture
def sample_backup_with_content(tmp_path: Path) -> BackupModel:
    backup_path = tmp_path / "backups" / "test_world" / "2026-04-22_12-00-00"
    backup_path.mkdir(parents=True, exist_ok=True)

    (backup_path / "level.dat").write_text("mock level data")
    (backup_path / "level.dat_old").write_text("old backup")

    world_dir = backup_path / "world"
    world_dir.mkdir()
    (world_dir / "chunk_file1.mcr").write_text("chunk data 1")
    (world_dir / "chunk_file2.mcr").write_text("chunk data 22")

    db_dir = backup_path / "db"
    db_dir.mkdir()
    (db_dir / "000000.ldb").write_text("database file")

    return BackupModel(
        world_folder_name="test_world",
        world_account_id="account123",
        created_at=datetime(2026, 4, 22, 12, 0, 0),
        backup_path=backup_path,
    )


@pytest.fixture
def backup_with_content(tmp_path: Path, sample_world: WorldModel) -> BackupModel:
    backup_path = tmp_path / "backups" / "backup_2026-04-20_10-30-00"
    backup_path.mkdir(parents=True)

    (backup_path / "level.dat").write_bytes(b"backup level data")
    (backup_path / "level.sdat").write_bytes(b"backup sdat data")
    subdir = backup_path / "world_data"
    subdir.mkdir()
    (subdir / "file.txt").write_text("content")

    return BackupModel(
        world_folder_name=sample_world.folder_name,
        world_account_id=sample_world.account_id,
        created_at=datetime(2026, 4, 20, 10, 30, 0),
        backup_path=backup_path,
    )
