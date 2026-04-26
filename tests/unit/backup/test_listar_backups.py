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

from backup_manager_mvp.core.models.backup_model import BackupModel
from backup_manager_mvp.core.models.world_model import WorldModel
from backup_manager_mvp.core.services.backup_service import BackupService
from backup_manager_mvp.infra.repository import FileSystemBackupRepository


class TestListBackups:
    def test_list_backups_returns_list(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        backup_base = tmp_path / "backups"

        from unittest.mock import patch

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.list_backups(sample_world)

        assert isinstance(result, list)

    def test_list_backups_returns_backup_models(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        backup_base = tmp_path / "backups"

        from unittest.mock import patch

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.list_backups(sample_world)

        assert isinstance(result, list)
        for backup in result:
            assert isinstance(backup, BackupModel)

    def test_list_backups_sorted_by_creation_date_newest_first(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        backup_base = tmp_path / "backups"
        world_backup_dir = backup_base / sample_world.levelname
        world_backup_dir.mkdir(parents=True)

        backup_times = [
            "2025-04-03_10-00-00",
            "2025-04-04_21-00-00",
            "2025-04-05_15-00-00",
        ]
        for backup_time in backup_times:
            (world_backup_dir / backup_time).mkdir()

        from unittest.mock import patch

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.list_backups(sample_world)

        if len(result) >= 2:
            for i in range(len(result) - 1):
                assert result[i].created_at >= result[i + 1].created_at

    def test_list_backups_empty_when_no_backups(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        backup_base = tmp_path / "backups"

        from unittest.mock import patch

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.list_backups(sample_world)

        assert isinstance(result, list)
        assert len(result) == 0


class TestListBackupsErrors:
    def test_list_backups_ignores_invalid_timestamp_folders(self, tmp_path: Path) -> None:
        service = BackupService(FileSystemBackupRepository())

        world = WorldModel(
            folder_name="xyz12345678=",
            levelname="Test World",
            path=tmp_path / "world",
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        from unittest.mock import patch

        with patch.object(service, "get_backup_base_path", return_value=tmp_path):
            backup_dir = tmp_path / world.folder_name
            backup_dir.mkdir()
            (backup_dir / "2025-01-01_12-00-00").mkdir()
            (backup_dir / "invalid_timestamp").mkdir()
            (backup_dir / "another_bad_name").mkdir()

            backups = service.list_backups(world)

            assert len(backups) == 1
            assert "2025-01-01_12-00-00" in str(backups[0].backup_path)

    def test_list_backups_handles_permission_error(self, tmp_path: Path) -> None:
        service = BackupService(FileSystemBackupRepository())

        world = WorldModel(
            folder_name="test1234567=",
            levelname="Test",
            path=tmp_path / "world",
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        from unittest.mock import patch

        with patch.object(service, "get_backup_base_path") as mock_path:
            backup_base = tmp_path / "backups"
            backup_base.mkdir()
            mock_path.return_value = backup_base

            backups = service.list_backups(world)
            assert backups == []

    def test_list_backups_ignores_non_directory_items(self, tmp_path: Path) -> None:
        service = BackupService(FileSystemBackupRepository())

        world = WorldModel(
            folder_name="test1234567=",
            levelname="TestWorld",
            path=tmp_path / "world",
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        backup_base = tmp_path / "backups"
        world_dir = backup_base / world.folder_name
        world_dir.mkdir(parents=True)

        valid_backup = world_dir / "2025-01-01_10-00-00"
        valid_backup.mkdir()

        (world_dir / "readme.txt").write_text("file")
        (world_dir / ".gitignore").write_text("ignored")

        from unittest.mock import patch

        with patch.object(service, "get_backup_base_path", return_value=backup_base):
            backups = service.list_backups(world)

        assert len(backups) == 1
        assert backups[0].backup_path == valid_backup
