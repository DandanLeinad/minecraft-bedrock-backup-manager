# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

from datetime import datetime

from backup_manager_mvp.core.models.backup_model import BackupModel
from backup_manager_mvp.core.services.backup_service import BackupService


class TestGetBackupPreviewInfo:
    """Tests for get_backup_preview_info method.

    Rules:
    - Returns a dictionary with backup metadata
    - Includes total_files, total_dirs, total_size, top_level_items, error
    - Counts files and directories correctly
    - Calculates total size recursively
    - Lists top-level items with name, type, size
    - Sorts directories before files
    - Handles non-existent backup (returns error)
    - Handles empty backup (no error)
    - Truncates large file lists (max 20 items + ellipsis)
    - Calculates size for directories
    """

    def test_should_return_dictionary_with_all_expected_keys(
        self, backup_service: BackupService, sample_backup_with_content: BackupModel
    ) -> None:
        """
        get_backup_preview_info should return a dictionary containing
        all expected keys: total_files, total_dirs, total_size,
        top_level_items, and error.
        """
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        assert isinstance(result, dict)
        assert "total_files" in result
        assert "total_dirs" in result
        assert "total_size" in result
        assert "top_level_items" in result
        assert "error" in result

    def test_should_count_files_correctly(
        self, backup_service: BackupService, sample_backup_with_content: BackupModel
    ) -> None:
        """
        get_backup_preview_info should count total files correctly.
        """
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        assert result["total_files"] == 5
        assert result["error"] is None

    def test_should_count_directories_correctly(
        self, backup_service: BackupService, sample_backup_with_content: BackupModel
    ) -> None:
        """
        get_backup_preview_info should count total directories correctly.
        """
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        assert result["total_dirs"] == 2
        assert result["error"] is None

    def test_should_calculate_total_size_correctly(
        self, backup_service: BackupService, sample_backup_with_content: BackupModel
    ) -> None:
        """
        get_backup_preview_info should calculate total size correctly.
        """
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        assert result["total_size"] == 63
        assert result["error"] is None

    def test_should_list_top_level_items_with_metadata(
        self, backup_service: BackupService, sample_backup_with_content: BackupModel
    ) -> None:
        """
        get_backup_preview_info should list top-level items with
        name, type, and size for each item.
        """
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        items = result["top_level_items"]
        assert len(items) == 4

        for item in items:
            assert "name" in item
            assert "type" in item
            assert "size" in item
            assert item["type"] in ("file", "dir")

    def test_should_sort_directories_before_files(
        self, backup_service: BackupService, sample_backup_with_content: BackupModel
    ) -> None:
        """
        get_backup_preview_info should sort directories before files
        in the top-level items list.
        """
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

    def test_should_return_error_for_nonexistent_backup(
        self, backup_service: BackupService, tmp_path
    ) -> None:
        """
        get_backup_preview_info should return error information
        when backup path does not exist.
        """
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

    def test_should_handle_empty_backup_without_error(
        self, backup_service: BackupService, tmp_path
    ) -> None:
        """
        get_backup_preview_info should handle empty backup directory
        without returning an error.
        """
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

    def test_should_truncate_large_file_lists(
        self, backup_service: BackupService, tmp_path
    ) -> None:
        """
        get_backup_preview_info should truncate large file lists
        to 20 items plus an ellipsis indicator.
        """
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

    def test_should_calculate_size_for_directories(
        self, backup_service: BackupService, sample_backup_with_content: BackupModel
    ) -> None:
        """
        get_backup_preview_info should calculate size for directories
        in top-level items.
        """
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        items = result["top_level_items"]
        world_item = next((i for i in items if i["name"] == "world"), None)

        assert world_item is not None
        assert world_item["size"] == 25
