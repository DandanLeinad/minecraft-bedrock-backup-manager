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

from datetime import datetime
from pathlib import Path

import pytest

from backup_manager_mvp.core.models.backup_model import BackupModel
from backup_manager_mvp.core.models.world_model import WorldModel
from backup_manager_mvp.core.services.backup_service import BackupService
from backup_manager_mvp.infra.repository import FileSystemBackupRepository


class TestRestoreBackup:
    @pytest.fixture
    def world_with_backup(
        self, tmp_path: Path, sample_world: WorldModel
    ) -> tuple[WorldModel, BackupModel]:
        current_file = sample_world.path / "level.dat"
        current_file.write_bytes(b"current world data")

        backup_path = tmp_path / "backups" / "backup_2025-04-04"
        backup_path.mkdir(parents=True)
        backup_file = backup_path / "level.dat"
        backup_file.write_bytes(b"backup world data")

        backup = BackupModel(
            world_folder_name=sample_world.folder_name,
            world_account_id=sample_world.account_id,
            created_at=datetime(2025, 4, 4, 21, 0, 0),
            backup_path=backup_path,
        )

        return sample_world, backup

    def test_restore_backup_returns_none(
        self, backup_service: BackupService, world_with_backup
    ) -> None:
        world, backup = world_with_backup

        result = backup_service.restore_backup(backup, world)

        assert result is None

    def test_restore_backup_replaces_world_contents(
        self, backup_service: BackupService, world_with_backup
    ) -> None:
        world, backup = world_with_backup

        backup_service.restore_backup(backup, world)

        restored_file = world.path / "level.dat"
        assert restored_file.exists()
        assert restored_file.read_bytes() == b"backup world data"

    def test_restore_backup_preserves_backup(
        self, backup_service: BackupService, world_with_backup
    ) -> None:
        world, backup = world_with_backup
        backup_file = backup.backup_path / "level.dat"

        backup_service.restore_backup(backup, world)

        assert backup_file.exists()
        assert backup_file.read_bytes() == b"backup world data"


class TestRestoreBackupErrors:
    def test_restore_backup_fails_if_backup_not_found(self) -> None:
        service = BackupService(FileSystemBackupRepository())

        backup = BackupModel(
            world_folder_name="test1234567=",
            world_account_id="test",
            created_at=datetime(2025, 1, 1, 12, 0, 0),
            backup_path=Path("/nonexistent/backup"),
        )

        world = WorldModel(
            folder_name="test1234567=",
            levelname="Test",
            path=Path("/some/path"),
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        with pytest.raises(FileNotFoundError, match="Backup não encontrado"):
            service.restore_backup(backup, world)

    def test_restore_backup_fails_if_world_not_found(self, tmp_path: Path) -> None:
        service = BackupService(FileSystemBackupRepository())

        backup_path = tmp_path / "backup"
        backup_path.mkdir()

        backup = BackupModel(
            world_folder_name="test1234567=",
            world_account_id="test",
            created_at=datetime(2025, 1, 1, 12, 0, 0),
            backup_path=backup_path,
        )

        world = WorldModel(
            folder_name="test1234567=",
            levelname="Test",
            path=tmp_path / "nonexistent_world",
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        with pytest.raises(FileNotFoundError, match="Mundo não encontrado"):
            service.restore_backup(backup, world)

    def test_restore_backup_handles_restore_error(self, tmp_path: Path) -> None:
        service = BackupService(FileSystemBackupRepository())

        backup_path = tmp_path / "backup"
        backup_path.mkdir()
        (backup_path / "subdir").mkdir()

        world_path = tmp_path / "world"
        world_path.mkdir()

        backup = BackupModel(
            world_folder_name="test1234567=",
            world_account_id="test",
            created_at=datetime(2025, 1, 1, 12, 0, 0),
            backup_path=backup_path,
        )

        world = WorldModel(
            folder_name="test1234567=",
            levelname="Test",
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        with pytest.raises(RuntimeError, match="Erro ao restaurar backup"):
            from unittest.mock import patch

            with patch.object(service.repository, "copy_tree") as mock_copytree:
                mock_copytree.side_effect = Exception("Copy failed")
                service.restore_backup(backup, world)

    def test_restore_backup_handles_copy2_error(self, tmp_path: Path) -> None:
        service = BackupService(FileSystemBackupRepository())

        backup_path = tmp_path / "backup"
        backup_path.mkdir()
        (backup_path / "file.txt").write_text("content")
        (backup_path / "subdir").mkdir()
        (backup_path / "subdir" / "inner.txt").write_text("inner")

        world_path = tmp_path / "world"
        world_path.mkdir()

        backup = BackupModel(
            world_folder_name="test1234567=",
            world_account_id="test",
            created_at=datetime(2025, 1, 1, 12, 0, 0),
            backup_path=backup_path,
        )

        world = WorldModel(
            folder_name="test1234567=",
            levelname="Test",
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        def mock_copy2_fail(src, dst):
            raise OSError("Permission denied")

        from unittest.mock import patch

        with (
            patch.object(service.repository, "copy_file", side_effect=mock_copy2_fail),
            pytest.raises(RuntimeError, match="Erro ao restaurar backup"),
        ):
            service.restore_backup(backup, world)
