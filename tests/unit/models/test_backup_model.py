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

from backup_manager_mvp.models.backup_model import BackupModel


@pytest.fixture
def valid_backup_data() -> dict:
    """Fixture com dados válidos para BackupModel."""
    return {
        "world_folder_name": "6LknJ-+T-Ks=",
        "world_account_id": "account123",
        "created_at": datetime(2025, 4, 4, 21, 0, 0),
        "backup_path": Path(
            "C:\\Users\\user\\Documents\\MinecraftBackups\\Meu Mundo\\2025-04-04_21-00-00"
        ),
    }


def test_backup_model_valid(valid_backup_data: dict) -> None:
    """Testa criação válida do BackupModel."""
    # Arrange (dados já fornecidos)

    # Act
    backup = BackupModel(**valid_backup_data)

    # Assert
    assert backup.world_folder_name == valid_backup_data["world_folder_name"]
    assert backup.world_account_id == valid_backup_data["world_account_id"]
    assert backup.created_at == valid_backup_data["created_at"]
    assert backup.backup_path == valid_backup_data["backup_path"]


@pytest.mark.parametrize(
    "field,invalid_value,test_id",
    [
        # Tipos inválidos
        ("world_folder_name", 123, "folder_name_type"),
        ("world_account_id", 123, "account_id_type"),
        # None
        ("world_folder_name", None, "folder_name_none"),
        ("world_account_id", None, "account_id_none"),
        ("created_at", None, "created_at_none"),
        ("backup_path", None, "backup_path_none"),
        # Vazio/whitespace
        ("world_folder_name", "", "folder_name_empty"),
        ("world_account_id", "", "account_id_empty"),
        ("world_folder_name", "   ", "folder_name_whitespace"),
        ("world_account_id", "   ", "account_id_whitespace"),
        # Path vazio
        ("backup_path", Path(""), "backup_path_empty"),
    ],
    ids=[
        "folder_name_type",
        "account_id_type",
        "folder_name_none",
        "account_id_none",
        "created_at_none",
        "backup_path_none",
        "folder_name_empty",
        "account_id_empty",
        "folder_name_whitespace",
        "account_id_whitespace",
        "backup_path_empty",
    ],
)
def test_backup_model_validation_error(
    field: str, invalid_value, test_id: str, valid_backup_data: dict
) -> None:
    """Testa que BackupModel rejeita valores inválidos.

    Testa diversos cenários de validação: tipos inválidos, None, vazios, whitespace.
    """
    # Arrange
    invalid_data = valid_backup_data.copy()
    invalid_data[field] = invalid_value

    # Act & Assert
    with pytest.raises(ValidationError):
        BackupModel(**invalid_data)


def test_backup_model_created_at_format_validation() -> None:
    """Testa que created_at deve ser um datetime válido."""
    # Arrange
    invalid_data = {
        "world_folder_name": "6LknJ-+T-Ks=",
        "world_account_id": "account123",
        "created_at": "invalid_datetime",
        "backup_path": Path(
            "C:\\Users\\user\\Documents\\MinecraftBackups\\Meu Mundo\\2025-04-04_21-00-00"
        ),
    }

    # Act & Assert
    with pytest.raises(ValidationError):
        BackupModel(**invalid_data)


class TestBackupModelSizeDisplay:
    """Testes para a propriedade size_display do BackupModel."""

    def test_backup_model_name_property(self, tmp_path: Path) -> None:
        """Testa a propriedade name que retorna o nome do diretório."""
        # Arrange
        backup_path = tmp_path / "2025-04-13_21-30-45"
        backup_path.mkdir()

        backup = BackupModel(
            world_folder_name="test_world=",
            world_account_id="account123",
            created_at=datetime.now(),
            backup_path=backup_path,
        )

        # Act
        name = backup.name

        # Assert
        assert name == "2025-04-13_21-30-45"

    def test_size_display_bytes(self, tmp_path: Path) -> None:
        """Testa formatação de tamanho em bytes (< 1024)."""
        # Arrange
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "file.txt").write_bytes(b"x" * 512)

        backup = BackupModel(
            world_folder_name="test_world=",
            world_account_id="account123",
            created_at=datetime.now(),
            backup_path=backup_dir,
        )

        # Act
        size = backup.size_display

        # Assert
        assert "B" in size
        assert not any(unit in size for unit in ["KB", "MB", "GB"])

    def test_size_display_kilobytes(self, tmp_path: Path) -> None:
        """Testa formatação de tamanho em KB (1024 to 1MB)."""
        # Arrange
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "file.txt").write_bytes(b"x" * (1024 * 50))  # 50 KB

        backup = BackupModel(
            world_folder_name="test_world=",
            world_account_id="account123",
            created_at=datetime.now(),
            backup_path=backup_dir,
        )

        # Act
        size = backup.size_display

        # Assert
        assert "KB" in size

    def test_size_display_megabytes(self, tmp_path: Path) -> None:
        """Testa formatação de tamanho em MB (1MB to 1GB)."""
        # Arrange
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "file.txt").write_bytes(b"x" * (1024 * 1024 * 5))  # 5 MB

        backup = BackupModel(
            world_folder_name="test_world=",
            world_account_id="account123",
            created_at=datetime.now(),
            backup_path=backup_dir,
        )

        # Act
        size = backup.size_display

        # Assert
        assert "MB" in size

    def test_size_display_gigabytes(self, tmp_path: Path) -> None:
        """Testa formatação de tamanho em GB (>= 1GB usando mock)."""
        from unittest.mock import patch

        # Arrange
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "file.txt").write_bytes(b"x")

        backup = BackupModel(
            world_folder_name="test_world=",
            world_account_id="account123",
            created_at=datetime.now(),
            backup_path=backup_dir,
        )

        # Act - Mock sum para retornar tamanho >= 1GB
        with patch("builtins.sum", return_value=2 * (1024**3)):
            size = backup.size_display

        # Assert
        assert "GB" in size

    def test_size_display_exception(self, tmp_path: Path) -> None:
        """Testa que exceção retorna 'N/A'."""
        from unittest.mock import patch

        # Arrange
        backup = BackupModel(
            world_folder_name="test_world=",
            world_account_id="account123",
            created_at=datetime.now(),
            backup_path=tmp_path / "backup",
        )

        # Act - Mock sum para lançar exceção
        with patch("builtins.sum", side_effect=OSError("Permission denied")):
            size = backup.size_display

        # Assert
        assert size == "N/A"
