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

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from backup_manager_mvp.core.models.backup_model import BackupModel
from backup_manager_mvp.core.models.world_model import WorldModel
from backup_manager_mvp.core.services.world_service import WorldService
from backup_manager_mvp.infra.repository import FileSystemWorldRepository


class TestGetWorldLevelname:
    """Tests for get_world_levelname method.

    Rules:
    - Returns levelname string from levelname.txt file
    - Raises FileNotFoundError when levelname.txt does not exist
    - Raises ValueError when file contains invalid UTF-8
    - Raises ValueError when file is empty or contains only whitespace
    """

    def test_should_return_levelname_when_file_exists(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """
        get_world_levelname should return the levelname string
        when levelname.txt file exists and is readable.
        """
        world_path = tmp_path / "test_world"
        world_path.mkdir()
        levelname_file = world_path / "levelname.txt"
        levelname_file.write_text("My World")

        result = world_service.get_world_levelname(world_path)

        assert isinstance(result, str)
        assert result == "My World"

    def test_should_read_levelname_from_file(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """
        get_world_levelname should read the exact content from levelname.txt.
        """
        world_path = tmp_path / "world"
        world_path.mkdir()
        levelname_file = world_path / "levelname.txt"
        expected_name = "Amazing World"
        levelname_file.write_text(expected_name, encoding="utf-8")

        result = world_service.get_world_levelname(world_path)

        assert result == expected_name

    def test_should_raise_file_not_found_when_levelname_missing(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """
        get_world_levelname should raise FileNotFoundError
        when levelname.txt does not exist.
        """
        world_path = tmp_path / "world"
        world_path.mkdir()

        with pytest.raises(FileNotFoundError):
            world_service.get_world_levelname(world_path)

    def test_should_raise_value_error_when_unicode_decode_error(self, tmp_path: Path) -> None:
        """
        get_world_levelname should raise ValueError
        when levelname.txt contains invalid UTF-8.
        """
        service = WorldService(FileSystemWorldRepository())

        world_path = tmp_path / "world"
        world_path.mkdir()
        levelname_file = world_path / "levelname.txt"
        levelname_file.write_bytes(b"\xff\xfe invalid utf-8")

        with pytest.raises(ValueError, match="Error decoding"):
            service.get_world_levelname(world_path)

    def test_should_raise_value_error_when_file_empty(self, tmp_path: Path) -> None:
        """
        get_world_levelname should raise ValueError
        when levelname.txt is empty or contains only whitespace.
        """
        service = WorldService(FileSystemWorldRepository())

        world_path = tmp_path / "world"
        world_path.mkdir()
        levelname_file = world_path / "levelname.txt"
        levelname_file.write_text("   \n\t  ")

        with pytest.raises(ValueError, match=r"vazio|whitespace"):
            service.get_world_levelname(world_path)


class TestGetWorldMetadata:
    """Tests for get_world_metadata method.

    Rules:
    - Returns size in human-readable format (B, KB, MB, GB)
    - Returns backups_count as string
    - Returns last_backup as relative time string in Portuguese
      (seconds: "há segundos", minutes: "Xm", hours: "Xh", days: "Xd")
    - Returns "N/A" for size when world path does not exist
    - Returns "0" and "Nunca" when no backups exist
    - Returns newest backup time when multiple backups exist
    - Handles backup service errors gracefully
    - Returns UWP store path with correct structure
    """

    def test_should_calculate_world_size_in_kilobytes(self, tmp_path: Path) -> None:
        """
        get_world_metadata should calculate world size in human-readable format.
        """
        service = WorldService(FileSystemWorldRepository())
        world_path = tmp_path / "world"
        world_path.mkdir()
        (world_path / "levelname.txt").write_text("Test World")
        (world_path / "file1.dat").write_bytes(b"x" * (1024 * 101))

        world = WorldModel(
            folder_name="testworld12=",
            levelname="Test World",
            world_icon_path=Path("world_icon.jpeg"),
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        metadata = service.get_world_metadata(world)

        assert "KB" in metadata["size"] or "MB" in metadata["size"]
        assert metadata["backups_count"] == "0"
        assert metadata["last_backup"] == "Nunca"

    def test_should_return_zero_backups_when_none_exist(self, tmp_path: Path) -> None:
        """
        get_world_metadata should return zero backups count and "Nunca"
        when no backups exist.
        """
        service = WorldService(FileSystemWorldRepository())
        world_path = tmp_path / "world"
        world_path.mkdir()
        (world_path / "levelname.txt").write_text("World")

        world = WorldModel(
            folder_name="world123456=",
            levelname="World",
            world_icon_path=Path("world_icon.jpeg"),
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        metadata = service.get_world_metadata(world, backup_service=None)

        assert metadata["backups_count"] == "0"
        assert metadata["last_backup"] == "Nunca"

    def test_should_show_recent_backup_as_seconds_ago(self, tmp_path: Path) -> None:
        """
        get_world_metadata should show "há segundos" for backups
        created within the last minute.
        """
        service = WorldService(FileSystemWorldRepository())
        world_path = tmp_path / "world"
        world_path.mkdir()
        (world_path / "levelname.txt").write_text("World")

        world = WorldModel(
            folder_name="world123456=",
            levelname="World",
            world_icon_path=Path("world_icon.jpeg"),
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        now = datetime.now()
        backup = BackupModel(
            world_folder_name=world.folder_name,
            world_account_id=world.account_id,
            created_at=now - timedelta(seconds=10),
            backup_path=Path("/tmp/backup1"),
        )

        class MockBackupService:
            def list_backups(self, w):
                return [backup]

        metadata = service.get_world_metadata(world, MockBackupService())

        assert metadata["backups_count"] == "1"
        assert metadata["last_backup"] == "há segundos"

    def test_should_return_newest_backup_when_multiple_exist(self, tmp_path: Path) -> None:
        """
        get_world_metadata should return the newest backup time
        when multiple backups exist.
        """
        service = WorldService(FileSystemWorldRepository())
        world_path = tmp_path / "world"
        world_path.mkdir()
        (world_path / "levelname.txt").write_text("World")

        world = WorldModel(
            folder_name="world123456=",
            levelname="World",
            world_icon_path=Path("world_icon.jpeg"),
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        now = datetime.now()
        backup_old = BackupModel(
            world_folder_name=world.folder_name,
            world_account_id=world.account_id,
            created_at=now - timedelta(days=5),
            backup_path=Path("/tmp/backup_old"),
        )
        backup_recent = BackupModel(
            world_folder_name=world.folder_name,
            world_account_id=world.account_id,
            created_at=now - timedelta(minutes=5),
            backup_path=Path("/tmp/backup_recent"),
        )

        class MockBackupService:
            def list_backups(self, w):
                return [backup_old, backup_recent]

        metadata = service.get_world_metadata(world, MockBackupService())

        assert metadata["backups_count"] == "2"
        assert "5m" in metadata["last_backup"]

    def test_should_return_na_for_nonexistent_world_path(self) -> None:
        """
        get_world_metadata should return "N/A" for size
        when world path does not exist.
        """
        service = WorldService(FileSystemWorldRepository())
        world = WorldModel(
            folder_name="nonexistent=",
            levelname="Nonexistent",
            world_icon_path=Path("world_icon.jpeg"),
            path=Path("/nonexistent/path/that/does/not/exist"),
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        metadata = service.get_world_metadata(world)

        assert metadata["size"] == "N/A"
        assert metadata["backups_count"] == "0"
        assert metadata["last_backup"] == "Nunca"

    def test_should_return_valid_uwp_store_path(self) -> None:
        """
        get_uwp_store_path should return a valid Path
        with Microsoft.MinecraftUWP_8wekyb3d8bbwe and minecraftWorlds in the path.
        """
        service = WorldService(FileSystemWorldRepository())

        uwp_path = service.get_uwp_store_path()

        assert isinstance(uwp_path, Path)
        assert "Microsoft.MinecraftUWP_8wekyb3d8bbwe" in str(uwp_path)
        assert "minecraftWorlds" in str(uwp_path)

    def test_should_handle_backup_service_error_gracefully(self, tmp_path: Path) -> None:
        """
        get_world_metadata should handle backup service errors gracefully
        by returning zero backups and "Nunca".
        """
        service = WorldService(FileSystemWorldRepository())
        world_path = tmp_path / "world"
        world_path.mkdir()
        (world_path / "levelname.txt").write_text("World")

        world = WorldModel(
            folder_name="world123456=",
            levelname="World",
            world_icon_path=Path("world_icon.jpeg"),
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        class BrokenBackupService:
            def list_backups(self, w):
                raise OSError("Error listing backups")

        metadata = service.get_world_metadata(world, BrokenBackupService())

        assert metadata["backups_count"] == "0"
        assert metadata["last_backup"] == "Nunca"

    def test_should_handle_all_time_deltas_correctly(self, tmp_path: Path) -> None:
        """
        get_world_metadata should format last_backup correctly
        for all time deltas (seconds, minutes, hours, days) in Portuguese.
        """
        service = WorldService(FileSystemWorldRepository())
        world_path = tmp_path / "world"
        world_path.mkdir()
        (world_path / "levelname.txt").write_text("World")

        world = WorldModel(
            folder_name="world123456=",
            levelname="World",
            world_icon_path=Path("world_icon.jpeg"),
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        now = datetime.now()

        test_cases = [
            (timedelta(seconds=5), "há segundos"),
            (timedelta(minutes=15), "há 15m"),
            (timedelta(hours=7), "há 7h"),
            (timedelta(days=3), "há 3d"),
        ]

        for delta, expected in test_cases:
            backup = BackupModel(
                world_folder_name="test",
                world_account_id="test",
                created_at=now - delta,
                backup_path=tmp_path / "backup",
            )

            class TestBackupService:
                def __init__(self, backup_model):
                    self._backup = backup_model

                def list_backups(self, w):
                    return [self._backup]

            metadata = service.get_world_metadata(world, TestBackupService(backup))
            assert metadata["last_backup"] == expected, f"Failed for delta {delta}"
