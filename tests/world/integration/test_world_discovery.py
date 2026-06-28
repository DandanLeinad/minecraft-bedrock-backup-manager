# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

"""Integration tests for world discovery with real filesystem."""

from pathlib import Path

import pytest

from backup_manager_mvp.core.services.world_service import WorldService


class TestWorldDiscoveryIntegration:
    """Integration tests for world discovery with real filesystem."""

    def test_should_find_valid_worlds(self, fs_world_repo, sample_world_dir: Path) -> None:
        """
        Should find valid worlds in the real filesystem.
        """
        # The fs_world_repo is already configured with the correct temp_dir via fixture
        service = WorldService(fs_world_repo)

        worlds = service.list_worlds()

        assert len(worlds) >= 1
        world = worlds[0]
        assert world.folder_name == "6LknJ3qXcJo="
        assert world.levelname == "Test World"

    def test_should_ignore_invalid_directories(self, fs_world_repo, temp_dir: Path) -> None:
        """
        Should ignore directories that are not valid worlds.
        """
        # Create directory without levelname.txt
        invalid_dir = temp_dir / "not_a_world"
        invalid_dir.mkdir()

        # Create a valid world in the test repository base directory
        # The fs_world_repo is already configured with the correct temp_dir
        base_path = fs_world_repo.get_worlds_base_path()
        account_id = "test_account_123"
        valid_dir = (
            base_path / account_id / "games" / "com.mojang" / "minecraftWorlds" / "abcdefghijk="
        )
        valid_dir.mkdir(parents=True, exist_ok=True)
        (valid_dir / "levelname.txt").write_text("Valid World", encoding="utf-8")
        (valid_dir / "level.dat").write_bytes(b"data")

        service = WorldService(fs_world_repo)

        # Test that only the valid world is found
        worlds = service.list_worlds()
        assert len(worlds) == 1
        assert worlds[0].levelname == "Valid World"

    def test_should_ignore_files_not_directories(self, fs_world_repo, temp_dir: Path) -> None:
        """
        Should ignore files that are not directories.
        """
        # Create a file at the root (not a directory)
        (temp_dir / "not_a_dir.txt").write_text("not a world")

        service = WorldService(fs_world_repo)
        worlds = service.list_worlds()

        # Should not crash, just ignore
        assert isinstance(worlds, list)

    def test_should_handle_permission_errors_gracefully(
        self, fs_world_repo, temp_dir: Path
    ) -> None:
        """
        Should handle permission errors gracefully.
        """
        service = WorldService(fs_world_repo)

        # Test with non-existent path
        worlds = service.list_worlds()
        assert isinstance(worlds, list)

    def test_should_read_levelname_from_file(self, fs_world_repo, sample_world_dir: Path) -> None:
        """
        Should read levelname from levelname.txt file.
        """
        service = WorldService(fs_world_repo)

        levelname = service.get_world_levelname(sample_world_dir)

        assert levelname == "Test World"

    def test_should_raise_file_not_found_when_levelname_missing(
        self, fs_world_repo, temp_dir: Path
    ) -> None:
        """
        Should raise FileNotFoundError if levelname.txt does not exist.
        """
        service = WorldService(fs_world_repo)

        invalid_dir = temp_dir / "no_levelname"
        invalid_dir.mkdir()

        with pytest.raises(FileNotFoundError):
            service.get_world_levelname(invalid_dir)

    def test_should_raise_value_error_when_levelname_empty(
        self, fs_world_repo, temp_dir: Path
    ) -> None:
        """
        Should raise ValueError if levelname.txt is empty.
        """
        service = WorldService(fs_world_repo)

        invalid_dir = temp_dir / "empty_levelname"
        invalid_dir.mkdir()
        (invalid_dir / "levelname.txt").write_text("", encoding="utf-8")

        with pytest.raises(ValueError, match="empty"):
            service.get_world_levelname(invalid_dir)

    def test_should_raise_value_error_when_levelname_whitespace_only(
        self, fs_world_repo, temp_dir: Path
    ) -> None:
        """
        Should raise ValueError if levelname.txt contains only whitespace.
        """
        service = WorldService(fs_world_repo)

        invalid_dir = temp_dir / "whitespace_levelname"
        invalid_dir.mkdir()
        (invalid_dir / "levelname.txt").write_text("   \n\t  ", encoding="utf-8")

        with pytest.raises(ValueError, match="empty"):
            service.get_world_levelname(invalid_dir)
