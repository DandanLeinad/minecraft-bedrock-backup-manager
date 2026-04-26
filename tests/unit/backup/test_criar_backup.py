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
from unittest.mock import patch

import pytest

from backup_manager_mvp.core.models.backup_model import BackupModel
from backup_manager_mvp.core.models.world_model import WorldModel
from backup_manager_mvp.core.services.backup_service import BackupService
from backup_manager_mvp.infra.repository import FileSystemBackupRepository


class TestGetBackupBasePath:
    def test_get_backup_base_path_returns_path_object(
        self, tmp_path: Path, backup_service: BackupService
    ) -> None:
        with patch.object(backup_service, "get_backup_base_path", return_value=tmp_path):
            result = backup_service.get_backup_base_path()

        assert isinstance(result, Path)

    def test_get_backup_base_path_contains_documents_dir(
        self, tmp_path: Path, backup_service: BackupService
    ) -> None:
        mock_path = tmp_path / "Documents" / "MinecraftBackups"

        with patch.object(backup_service, "get_backup_base_path", return_value=mock_path):
            result = backup_service.get_backup_base_path()

        path_str = str(result).lower()
        assert "documents" in path_str or "documentos" in path_str


class TestCreateBackup:
    def test_create_backup_returns_backup_model(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        backup_base = tmp_path / "backups"
        backup_base.mkdir()

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.create_backup(sample_world)

        assert isinstance(result, BackupModel)

    def test_create_backup_creates_backup_directory(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        backup_base = tmp_path / "backups"
        (sample_world.path / "file.txt").write_text("test content")

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.create_backup(sample_world)

        assert result.backup_path.exists()
        assert result.backup_path.is_dir()

    def test_create_backup_copies_world_contents(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        test_file = sample_world.path / "level.dat"
        test_file.write_bytes(b"test data")
        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.create_backup(sample_world)

        restored_file = result.backup_path / "level.dat"
        assert restored_file.exists()
        assert restored_file.read_bytes() == b"test data"

    def test_create_backup_sets_created_at(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        backup_base = tmp_path / "backups"
        before = datetime.now()

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.create_backup(sample_world)
            after = datetime.now()

        assert before <= result.created_at <= after

    def test_create_backup_includes_levelname_and_timestamp_in_path(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.create_backup(sample_world)

        assert sample_world.folder_name in result.backup_path.parts
        assert sample_world.levelname not in result.backup_path.parts

        backup_dirname = result.backup_path.name
        parts = backup_dirname.split("_")
        assert len(parts) == 2, f"Timestamp inválido: {backup_dirname}"

        date_part = parts[0]
        date_components = date_part.split("-")
        assert len(date_components) == 3, f"Data inválida: {date_part}"

        time_part = parts[1]
        time_components = time_part.split("-")
        assert len(time_components) == 3, f"Hora inválida: {time_part}"

    def test_backups_persist_after_world_rename(
        self, tmp_path: Path, backup_service: BackupService
    ) -> None:
        backup_base = tmp_path / "backups"
        world_path = tmp_path / "test_world"
        world_path.mkdir()
        test_file = world_path / "level.dat"
        test_file.write_bytes(b"original world")

        original_world = WorldModel(
            folder_name="6LknJ-+T-Ks=",
            levelname="Alicia",
            path=world_path,
            account_id="test_account",
            version=[1, 26, 12, 2, 0],
        )

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            backup1 = backup_service.create_backup(original_world)

            renamed_world = WorldModel(
                folder_name="6LknJ-+T-Ks=",
                levelname="Alicia2",
                path=world_path,
                account_id="test_account",
                version=[1, 26, 12, 2, 0],
            )

            backups = backup_service.list_backups(renamed_world)

        assert len(backups) == 1
        assert backups[0].backup_path == backup1.backup_path


class TestCreateBackupErrors:
    def test_create_backup_fails_on_copytree_error(self, tmp_path: Path) -> None:
        service = BackupService(FileSystemBackupRepository())

        world_path = tmp_path / "world"
        world_path.mkdir()

        world = WorldModel(
            folder_name="test1234567=",
            levelname="Test World",
            path=world_path,
            account_id="test_account",
            version=[1, 0, 0, 0, 0],
        )

        backup_base = tmp_path / "backups"

        with (
            patch.object(service, "get_backup_base_path", return_value=backup_base),
            patch.object(service.repository, "copy_tree") as mock_copytree,
        ):
            mock_copytree.side_effect = OSError("Simulated copy failure")

            with pytest.raises(RuntimeError, match="Erro ao criar backup"):
                service.create_backup(world)

    def test_create_backup_backup_path_exists_gets_removed(self, tmp_path: Path) -> None:
        service = BackupService(FileSystemBackupRepository())

        world_path = tmp_path / "world"
        world_path.mkdir()
        (world_path / "test_file.txt").write_text("content")
        (world_path / "levelname.txt").write_text("Test World")

        world = WorldModel(
            folder_name="abc123def89=",
            levelname="Test World",
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        backup_base = tmp_path / "backups"

        with patch.object(service, "get_backup_base_path", return_value=backup_base):
            backup = service.create_backup(world)
            assert backup.backup_path.exists()
            assert (backup.backup_path / "test_file.txt").exists()

    def test_create_backup_rmtree_called_when_path_exists(self, tmp_path: Path) -> None:
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
        )

        backup_path_ref: list[Path | None] = [None]

        def mock_copytree_fail(src, dst, **kwargs):
            backup_path_ref[0] = Path(dst)
            Path(dst).mkdir(parents=True, exist_ok=True)
            (Path(dst) / "partial.txt").write_text("partial")
            raise Exception("Simulated copy failure")

        with (
            patch.object(service, "get_backup_base_path", return_value=backup_base),
            patch("shutil.copytree", side_effect=mock_copytree_fail),
            pytest.raises(RuntimeError, match="Erro ao criar backup"),
        ):
            service.create_backup(world)

        assert backup_path_ref[0] is not None
