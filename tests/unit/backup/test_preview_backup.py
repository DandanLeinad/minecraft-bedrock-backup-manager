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

from backup_manager_mvp.core.models.backup_model import BackupModel
from backup_manager_mvp.core.services.backup_service import BackupService


class TestGetBackupPreviewInfo:
    def test_get_backup_preview_info_returns_dict(
        self, backup_service: BackupService, sample_backup_with_content: BackupModel
    ) -> None:
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        assert isinstance(result, dict)
        assert "total_files" in result
        assert "total_dirs" in result
        assert "total_size" in result
        assert "top_level_items" in result
        assert "error" in result

    def test_get_backup_preview_info_counts_files_correctly(
        self, backup_service: BackupService, sample_backup_with_content: BackupModel
    ) -> None:
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        assert result["total_files"] == 5
        assert result["error"] is None

    def test_get_backup_preview_info_counts_dirs_correctly(
        self, backup_service: BackupService, sample_backup_with_content: BackupModel
    ) -> None:
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        assert result["total_dirs"] == 2
        assert result["error"] is None

    def test_get_backup_preview_info_calculates_size(
        self, backup_service: BackupService, sample_backup_with_content: BackupModel
    ) -> None:
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        assert result["total_size"] == 63
        assert result["error"] is None

    def test_get_backup_preview_info_lists_top_level_items(
        self, backup_service: BackupService, sample_backup_with_content: BackupModel
    ) -> None:
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        items = result["top_level_items"]
        assert len(items) == 4

        for item in items:
            assert "name" in item
            assert "type" in item
            assert "size" in item
            assert item["type"] in ("file", "dir")

    def test_get_backup_preview_info_sorts_dirs_first(
        self, backup_service: BackupService, sample_backup_with_content: BackupModel
    ) -> None:
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        items = result["top_level_items"]
        for item in items:
            if item["type"] == "dir":
                assert True
            elif item["type"] == "file":
                remaining = items[items.index(item) + 1 :]
                for remaining_item in remaining:
                    assert remaining_item["type"] != "dir"
                break

    def test_get_backup_preview_info_nonexistent_backup(
        self, backup_service: BackupService, tmp_path
    ) -> None:
        backup_path = tmp_path / "nonexistent"

        backup = BackupModel(
            world_folder_name="nonexistent_world",
            world_account_id="account123",
            created_at=datetime(2026, 4, 22, 12, 0, 0),
            backup_path=backup_path,
        )

        result = backup_service.get_backup_preview_info(backup)

        assert result["total_files"] == 0
        assert result["total_dirs"] == 0
        assert result["total_size"] == 0
        assert result["top_level_items"] == []
        assert result["error"] is not None

    def test_get_backup_preview_info_empty_backup(
        self, backup_service: BackupService, tmp_path
    ) -> None:
        backup_path = tmp_path / "empty_backup"
        backup_path.mkdir(parents=True, exist_ok=True)

        backup = BackupModel(
            world_folder_name="empty_world",
            world_account_id="account123",
            created_at=datetime(2026, 4, 22, 12, 0, 0),
            backup_path=backup_path,
        )

        result = backup_service.get_backup_preview_info(backup)

        assert result["total_files"] == 0
        assert result["total_dirs"] == 0
        assert result["total_size"] == 0
        assert result["top_level_items"] == []
        assert result["error"] is None

    def test_get_backup_preview_info_large_file_list_truncated(
        self, backup_service: BackupService, tmp_path
    ) -> None:
        backup_path = tmp_path / "many_files_backup"
        backup_path.mkdir(parents=True, exist_ok=True)

        for i in range(25):
            (backup_path / f"file_{i}.dat").write_text(f"content {i}")

        backup = BackupModel(
            world_folder_name="many_files",
            world_account_id="account123",
            created_at=datetime(2026, 4, 22, 12, 0, 0),
            backup_path=backup_path,
        )

        result = backup_service.get_backup_preview_info(backup)

        assert len(result["top_level_items"]) == 21
        assert result["top_level_items"][-1]["type"] == "ellipsis"
        assert result["top_level_items"][-1]["name"] == "... e mais itens"

    def test_get_backup_preview_info_size_calculated_for_dirs(
        self, backup_service: BackupService, sample_backup_with_content: BackupModel
    ) -> None:
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        items = result["top_level_items"]
        world_item = next((i for i in items if i["name"] == "world"), None)

        assert world_item is not None
        assert world_item["size"] == 25
