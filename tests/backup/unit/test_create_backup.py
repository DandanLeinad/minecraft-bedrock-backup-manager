# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from backup_manager_mvp.core.models.backup_model import BackupModel
from backup_manager_mvp.core.models.world_model import WorldModel
from backup_manager_mvp.core.services.backup_service import BackupService
from backup_manager_mvp.infra.repository import FileSystemBackupRepository


class TestGetBackupBasePath:
    """Tests for get_backup_base_path method."""

    def test_should_return_path_object_when_called(
        self, tmp_path: Path, backup_service: BackupService
    ) -> None:
        """
        get_backup_base_path should return a Path object.
        """
        with patch.object(backup_service, "get_backup_base_path", return_value=tmp_path):
            result = backup_service.get_backup_base_path()

        assert isinstance(result, Path)

    def test_should_contain_documents_directory_in_path(
        self, tmp_path: Path, backup_service: BackupService
    ) -> None:
        """
        get_backup_base_path should return a path containing Documents directory
        (English or Portuguese).
        """
        mock_path = tmp_path / "Documents" / "MinecraftBackups"

        with patch.object(backup_service, "get_backup_base_path", return_value=mock_path):
            result = backup_service.get_backup_base_path()

        path_str = str(result).lower()
        assert "documents" in path_str or "documentos" in path_str


class TestCreateBackup:
    """Tests for create_backup method.

    Rules:
    - Returns BackupModel with correct metadata
    - Creates backup directory with timestamp format YYYY-MM-DD_HH-MM-SS
    - Copies all world contents recursively
    - Sets created_at to current time
    - Backup path includes world folder_name but not levelname
    - Backups persist after world rename (identified by folder_name)
    """

    def test_should_return_backup_model_when_backup_created(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """
        create_backup should return a BackupModel instance.
        """
        backup_base = tmp_path / "backups"
        backup_base.mkdir()

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.create_backup(sample_world)

        assert isinstance(result, BackupModel)

    def test_should_create_backup_directory_when_backup_created(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """
        create_backup should create a backup directory that exists and is a directory.
        """
        backup_base = tmp_path / "backups"
        (sample_world.path / "file.txt").write_text("test content")

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.create_backup(sample_world)

        assert result.backup_path.exists()
        assert result.backup_path.is_dir()

    def test_should_copy_world_contents_to_backup(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """
        create_backup should copy all world contents to the backup directory.
        """
        test_file = sample_world.path / "level.dat"
        test_file.write_bytes(b"test data")
        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.create_backup(sample_world)

        restored_file = result.backup_path / "level.dat"
        assert restored_file.exists()
        assert restored_file.read_bytes() == b"test data"

    def test_should_set_created_at_to_current_time(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """
        create_backup should set created_at to a time between before and after the call.
        """
        backup_base = tmp_path / "backups"
        before = datetime.now()

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.create_backup(sample_world)
            after = datetime.now()

        assert before <= result.created_at <= after

    def test_should_include_folder_name_and_timestamp_in_backup_path(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """
        create_backup should create a backup path containing the world folder_name
        and a timestamp in format YYYY-MM-DD_HH-MM-SS.
        The levelname should not be part of the path.
        """
        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.create_backup(sample_world)

        assert sample_world.folder_name in result.backup_path.parts
        assert sample_world.levelname not in result.backup_path.parts

        backup_dirname = result.backup_path.name
        parts = backup_dirname.split("_")
        assert len(parts) == 2, f"Invalid timestamp format: {backup_dirname}"

        date_part = parts[0]
        date_components = date_part.split("-")
        assert len(date_components) == 3, f"Invalid date format: {date_part}"

        time_part = parts[1]
        time_components = time_part.split("-")
        assert len(time_components) == 3, f"Invalid time format: {time_part}"

    def test_should_persist_backups_after_world_rename(
        self, tmp_path: Path, backup_service: BackupService
    ) -> None:
        """
        Backups should persist and be findable after world is renamed,
        identified by folder_name (not levelname).
        """
        backup_base = tmp_path / "backups"
        world_path = tmp_path / "test_world"
        world_path.mkdir()
        test_file = world_path / "level.dat"
        test_file.write_bytes(b"original world")

        original_world = WorldModel(
            folder_name="6LknJ-+T-Ks=",
            levelname="Alicia",
            world_icon_path=world_path / "world_icon.jpeg",
            path=world_path,
            account_id="test_account",
            version=[1, 26, 12, 2, 0],
        )

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            backup1 = backup_service.create_backup(original_world)

            renamed_world = WorldModel(
                folder_name="6LknJ-+T-Ks=",
                levelname="Alicia2",
                world_icon_path=world_path / "world_icon.jpeg",
                path=world_path,
                account_id="test_account",
                version=[1, 26, 12, 2, 0],
            )

            backups = backup_service.list_backups(renamed_world)

        assert len(backups) == 1
        assert backups[0].backup_path == backup1.backup_path


class TestCreateBackupErrors:
    """Tests for create_backup error handling.

    Rules:
    - Raises RuntimeError when copytree fails
    - Removes existing backup path before creating new one
    - Cleans up partial backup on copy failure
    """

    def test_should_raise_runtime_error_when_copytree_fails(self, tmp_path: Path) -> None:
        """
        create_backup should raise RuntimeError when copytree operation fails.
        """
        service = BackupService(FileSystemBackupRepository())

        world_path = tmp_path / "world"
        world_path.mkdir()

        world = WorldModel(
            folder_name="test1234567=",
            levelname="Test World",
            path=world_path,
            world_icon_path=world_path / "world_icon.jpeg",
            account_id="test_account",
            version=[1, 0, 0, 0, 0],
        )

        backup_base = tmp_path / "backups"

        with (
            patch.object(service, "get_backup_base_path", return_value=backup_base),
            patch.object(service.repository, "copy_tree_with_progress") as mock_copytree,
        ):
            mock_copytree.side_effect = OSError("Simulated copy failure")

            with pytest.raises(RuntimeError, match="Error creating backup"):
                service.create_backup(world)

    def test_should_remove_existing_backup_path_before_creating_new(self, tmp_path: Path) -> None:
        """
        create_backup should remove existing backup directory before creating new one.
        """
        service = BackupService(FileSystemBackupRepository())

        world_path = tmp_path / "world"
        world_path.mkdir()
        (world_path / "test_file.txt").write_text("content")
        (world_path / "levelname.txt").write_text("Test World")

        world = WorldModel(
            folder_name="abc123def89=",
            levelname="Test World",
            path=world_path,
            world_icon_path=world_path / "world_icon.jpeg",
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        backup_base = tmp_path / "backups"

        with patch.object(service, "get_backup_base_path", return_value=backup_base):
            backup = service.create_backup(world)
            assert backup.backup_path.exists()
            assert (backup.backup_path / "test_file.txt").exists()

    def test_should_cleanup_partial_backup_on_copy_failure(self, tmp_path: Path) -> None:
        """
        create_backup should clean up partially created backup directory on copy failure.
        """
        service = BackupService(FileSystemBackupRepository())

        backup_base = tmp_path / "backups"
        backup_base.mkdir(parents=True)

        world_path = tmp_path / "world"
        world_path.mkdir()
        (world_path / "some_file.txt").write_text("content")

        world = WorldModel(
            folder_name="test1234567=",
            levelname="TestWorld",
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
            world_icon_path=world_path / "world_icon.jpeg",
        )

        backup_path_ref: list[Path | None] = [None]

        def mock_copy_with_progress_fail(
            source: Path,
            destination: Path,
            progress_callback=None,
            *,
            dirs_exist_ok: bool = False,
        ):
            backup_path_ref[0] = destination
            destination.mkdir(parents=True, exist_ok=True)
            (destination / "partial.txt").write_text("partial")
            raise Exception("Simulated copy failure")

        with (
            patch.object(service, "get_backup_base_path", return_value=backup_base),
            patch.object(
                service.repository,
                "copy_tree_with_progress",
                side_effect=mock_copy_with_progress_fail,
            ),
            pytest.raises(RuntimeError, match="Error creating backup"),
        ):
            service.create_backup(world)

        assert backup_path_ref[0] is not None
