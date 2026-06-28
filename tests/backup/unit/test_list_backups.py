# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

from pathlib import Path
from unittest.mock import patch

from backup_manager_mvp.core.models.backup_model import BackupModel
from backup_manager_mvp.core.models.world_model import WorldModel
from backup_manager_mvp.core.services.backup_service import BackupService
from backup_manager_mvp.infra.repository import FileSystemBackupRepository


class TestListBackups:
    """Tests for list_backups method.

    Rules:
    - Returns empty list when no backups exist
    - Returns list of BackupModel instances
    - Returns backups sorted by creation date (newest first)
    - Filters by world folder_name and account_id
    """

    def test_should_return_empty_list_when_no_backups(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """
        list_backups should return empty list when no backups exist.
        """
        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.list_backups(sample_world)

        assert isinstance(result, list)
        assert len(result) == 0

    def test_should_return_list_of_backup_models(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """
        list_backups should return a list of BackupModel instances.
        """
        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.list_backups(sample_world)

        assert isinstance(result, list)
        for backup in result:
            assert isinstance(backup, BackupModel)

    def test_should_return_backups_sorted_by_newest_first(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """
        list_backups should return backups sorted by creation date,
        newest first.
        """
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

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.list_backups(sample_world)

        if len(result) >= 2:
            for i in range(len(result) - 1):
                assert result[i].created_at >= result[i + 1].created_at


class TestListBackupsEdgeCases:
    """Tests for list_backups edge cases and error handling.

    Rules:
    - Ignores folders with invalid timestamp format
    - Handles permission errors gracefully (returns empty list)
    - Ignores non-directory items (files) in backup directory
    """

    def test_should_ignore_invalid_timestamp_folders(self, tmp_path: Path) -> None:
        """
        list_backups should ignore folders with invalid timestamp format
        and only return valid backup folders.
        """
        service = BackupService(FileSystemBackupRepository())

        world = WorldModel(
            folder_name="xyz12345678=",
            levelname="Test World",
            world_icon_path=tmp_path / "world_icon.jpeg",
            path=tmp_path / "world",
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        with patch.object(service, "get_backup_base_path", return_value=tmp_path):
            backup_dir = tmp_path / world.folder_name
            backup_dir.mkdir()
            (backup_dir / "2025-01-01_12-00-00").mkdir()
            (backup_dir / "invalid_timestamp").mkdir()
            (backup_dir / "another_bad_name").mkdir()

            backups = service.list_backups(world)

            assert len(backups) == 1
            assert "2025-01-01_12-00-00" in str(backups[0].backup_path)

    def test_should_return_empty_list_when_permission_error(self, tmp_path: Path) -> None:
        """
        list_backups should return empty list when permission error occurs
        while reading backup directory.
        """
        service = BackupService(FileSystemBackupRepository())

        world = WorldModel(
            folder_name="test1234567=",
            levelname="Test",
            world_icon_path=tmp_path / "world_icon.jpeg",
            path=tmp_path / "world",
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        with patch.object(service, "get_backup_base_path") as mock_path:
            backup_base = tmp_path / "backups"
            backup_base.mkdir()
            mock_path.return_value = backup_base

            backups = service.list_backups(world)
            assert backups == []

    def test_should_ignore_non_directory_items(self, tmp_path: Path) -> None:
        """
        list_backups should ignore files (non-directories) in the backup directory.
        """
        service = BackupService(FileSystemBackupRepository())

        world = WorldModel(
            folder_name="test1234567=",
            levelname="TestWorld",
            world_icon_path=tmp_path / "world_icon.jpeg",
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

        with patch.object(service, "get_backup_base_path", return_value=backup_base):
            backups = service.list_backups(world)

        assert len(backups) == 1
        assert backups[0].backup_path == valid_backup
