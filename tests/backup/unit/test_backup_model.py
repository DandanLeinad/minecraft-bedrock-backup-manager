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
from pydantic import ValidationError

from backup_manager_mvp.core.models.backup_model import BackupModel


@pytest.fixture
def valid_backup_data() -> dict:
    return {
        "world_folder_name": "6LknJ-+T-Ks=",
        "world_account_id": "account123",
        "created_at": datetime(2025, 4, 4, 21, 0, 0),
        "backup_path": Path(
            "C:\\Users\\user\\Documents\\MinecraftBackups\\Meu Mundo\\2025-04-04_21-00-00"
        ),
    }


class TestBackupModelConstruction:
    """Tests for valid BackupModel creation."""

    def test_should_create_backup_model_when_all_fields_valid(
        self, valid_backup_data: dict
    ) -> None:
        """
        A valid BackupModel should be created when all required fields
        are provided with valid values.
        """
        backup = BackupModel(**valid_backup_data)

        assert backup.world_folder_name == valid_backup_data["world_folder_name"]
        assert backup.world_account_id == valid_backup_data["world_account_id"]
        assert backup.created_at == valid_backup_data["created_at"]
        assert backup.backup_path == valid_backup_data["backup_path"]

    def test_should_reject_backup_model_when_created_at_invalid(
        self, valid_backup_data: dict
    ) -> None:
        """
        BackupModel should reject creation when created_at is not a valid datetime.
        """
        invalid_data = valid_backup_data.copy()
        invalid_data["created_at"] = "invalid_datetime"

        with pytest.raises(ValidationError):
            BackupModel(**invalid_data)


class TestBackupModelFieldValidation:
    """Tests for BackupModel field validation rules.

    Rules:
    - world_folder_name: must be string, not None, not empty, not whitespace only
    - world_account_id: must be string, not None, not empty, not whitespace only
    - created_at: must be datetime, not None
    - backup_path: must be Path, not None, not empty
    """

    @pytest.mark.parametrize(
        "field,invalid_value,description",
        [
            ("world_folder_name", 123, "type_int"),
            ("world_account_id", 123, "type_int"),
            ("world_folder_name", None, "none"),
            ("world_account_id", None, "none"),
            ("created_at", None, "none"),
            ("backup_path", None, "none"),
            ("world_folder_name", "", "empty"),
            ("world_account_id", "", "empty"),
            ("world_folder_name", "   ", "whitespace_only"),
            ("world_account_id", "   ", "whitespace_only"),
            ("backup_path", Path(""), "empty"),
        ],
        ids=[
            "world_folder_name_type_int",
            "world_account_id_type_int",
            "world_folder_name_none",
            "world_account_id_none",
            "created_at_none",
            "backup_path_none",
            "world_folder_name_empty",
            "world_account_id_empty",
            "world_folder_name_whitespace_only",
            "world_account_id_whitespace_only",
            "backup_path_empty",
        ],
    )
    def test_should_reject_invalid_field_values(
        self, field: str, invalid_value, description: str, valid_backup_data: dict
    ) -> None:
        """
        BackupModel should reject invalid values for all fields:
        - wrong type (int instead of string)
        - None values
        - empty strings
        - whitespace-only strings
        - empty Path
        """
        invalid_data = valid_backup_data.copy()
        invalid_data[field] = invalid_value

        with pytest.raises(ValidationError):
            BackupModel(**invalid_data)


class TestBackupModelProperties:
    """Tests for BackupModel computed properties."""

    def test_should_return_backup_name_from_path_timestamp(self, tmp_path: Path) -> None:
        """
        name property should return the backup directory name (timestamp).
        """
        backup_path = tmp_path / "2025-04-13_21-30-45"
        backup_path.mkdir()

        backup = BackupModel(
            world_folder_name="test_world=",
            world_account_id="account123",
            created_at=datetime.now(),
            backup_path=backup_path,
        )

        assert backup.name == "2025-04-13_21-30-45"

    def test_should_display_size_in_bytes_when_under_kilobyte(self, tmp_path: Path) -> None:
        """
        size_display should show size in bytes when under 1 KB.
        """
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "file.txt").write_bytes(b"x" * 512)

        backup = BackupModel(
            world_folder_name="test_world=",
            world_account_id="account123",
            created_at=datetime.now(),
            backup_path=backup_dir,
        )

        size = backup.size_display

        assert "B" in size
        assert not any(unit in size for unit in ["KB", "MB", "GB"])

    def test_should_display_size_in_kilobytes_when_under_megabyte(self, tmp_path: Path) -> None:
        """
        size_display should show size in KB when under 1 MB.
        """
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "file.txt").write_bytes(b"x" * (1024 * 50))

        backup = BackupModel(
            world_folder_name="test_world=",
            world_account_id="account123",
            created_at=datetime.now(),
            backup_path=backup_dir,
        )

        size = backup.size_display

        assert "KB" in size

    def test_should_display_size_in_megabytes_when_under_gigabyte(self, tmp_path: Path) -> None:
        """
        size_display should show size in MB when under 1 GB.
        """
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "file.txt").write_bytes(b"x" * (1024 * 1024 * 5))

        backup = BackupModel(
            world_folder_name="test_world=",
            world_account_id="account123",
            created_at=datetime.now(),
            backup_path=backup_dir,
        )

        size = backup.size_display

        assert "MB" in size

    def test_should_display_size_in_gigabytes_when_large(self, tmp_path: Path) -> None:
        """
        size_display should show size in GB when 1 GB or larger.
        """
        from unittest.mock import patch

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "file.txt").write_bytes(b"x")

        backup = BackupModel(
            world_folder_name="test_world=",
            world_account_id="account123",
            created_at=datetime.now(),
            backup_path=backup_dir,
        )

        with patch("builtins.sum", return_value=2 * (1024**3)):
            size = backup.size_display

        assert "GB" in size

    def test_should_return_na_when_size_calculation_fails(self, tmp_path: Path) -> None:
        """
        size_display should return "N/A" when size calculation fails.
        """
        from unittest.mock import patch

        backup = BackupModel(
            world_folder_name="test_world=",
            world_account_id="account123",
            created_at=datetime.now(),
            backup_path=tmp_path / "backup",
        )

        with patch("builtins.sum", side_effect=OSError("Permission denied")):
            size = backup.size_display

        assert size == "N/A"
