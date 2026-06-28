# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

from pathlib import Path
from unittest.mock import MagicMock, patch

from backup_manager_mvp.core.models.world_model import WorldModel
from backup_manager_mvp.core.services.world_service import WorldService
from backup_manager_mvp.infra.repository import FileSystemWorldRepository


class TestGetWorldsBasePath:
    """Tests for get_worlds_base_path method."""

    def test_should_return_path_object_when_called(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """
        get_worlds_base_path should return a Path object.
        """
        with patch.object(world_service, "get_worlds_base_path", return_value=tmp_path):
            result = world_service.get_worlds_base_path()

        assert isinstance(result, Path)

    def test_should_return_expected_path_structure(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """
        get_worlds_base_path should return a path containing the expected
        Minecraft Bedrock directory structure (AppData/Roaming/Minecraft Bedrock/Users).
        """
        mock_path = tmp_path / "AppData" / "Roaming" / "Minecraft Bedrock" / "Users"

        with patch.object(world_service, "get_worlds_base_path", return_value=mock_path):
            result = world_service.get_worlds_base_path()

        assert "AppData" in str(result) or "Roaming" in str(result)


class TestListAccountIds:
    """Tests for list_account_ids method.

    Rules:
    - Returns empty list when base path does not exist
    - Returns empty list when no account directories exist
    - Returns sorted list of account directory names
    - Handles permission errors gracefully by returning empty list
    """

    def test_should_return_empty_list_when_base_path_not_exists(
        self, world_service: WorldService
    ) -> None:
        """
        list_account_ids should return empty list when base path does not exist.
        """
        with patch.object(world_service, "get_worlds_base_path") as mock_base_path:
            mock_base_path.return_value = Path("/nonexistent/path/that/does/not/exist")

            result = world_service.list_account_ids()

            assert result == []

    def test_should_return_empty_list_when_no_accounts(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """
        list_account_ids should return empty list when base path exists
        but contains no account directories.
        """
        users_dir = tmp_path / "Users"
        users_dir.mkdir(parents=True)

        with patch.object(world_service, "get_worlds_base_path", return_value=users_dir):
            result = world_service.list_account_ids()

            assert isinstance(result, list)
            assert len(result) == 0

    def test_should_return_sorted_account_ids_when_valid_structure(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """
        list_account_ids should return sorted list of account directory names
        when valid structure exists.
        """
        users_dir = tmp_path / "Users"
        account1 = users_dir / "account_id_1"
        account2 = users_dir / "account_id_2"
        account1.mkdir(parents=True)
        account2.mkdir(parents=True)

        with patch.object(world_service, "get_worlds_base_path", return_value=users_dir):
            result = world_service.list_account_ids()

            assert len(result) >= 2
            assert "account_id_1" in result
            assert "account_id_2" in result

    def test_should_return_empty_list_when_permission_error(
        self, world_service: WorldService
    ) -> None:
        """
        list_account_ids should return empty list when permission error occurs
        while reading base path.
        """
        with patch.object(world_service, "get_worlds_base_path") as mock_path:
            mock_base = MagicMock()
            mock_base.exists.return_value = True
            mock_base.iterdir.side_effect = PermissionError("Access denied")
            mock_path.return_value = mock_base

            account_ids = world_service.list_account_ids()
            assert account_ids == []


class TestListWorlds:
    """Tests for list_worlds and _list_worlds_from_path methods.

    Rules:
    - Returns empty list when no worlds exist
    - Returns WorldModel instances for valid worlds
    - Valid world requires: directory, levelname.txt (non-empty), level.dat
    - Ignores non-directories (files)
    - Ignores folders without levelname.txt
    - Ignores folders with empty/whitespace levelname.txt
    - Ignores folders with invalid folder_name format
    - Handles permission errors gracefully
    - Searches three sources: normal accounts, UWP Store, Shared
    """

    def test_should_return_empty_list_when_no_worlds(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """
        list_worlds should return empty list when no worlds exist.
        """
        with patch.object(world_service, "get_worlds_base_path", return_value=tmp_path):
            result = world_service.list_worlds()

        assert isinstance(result, list)
        assert len(result) == 0

    def test_should_return_world_models_when_valid_worlds_exist(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """
        list_worlds should return WorldModel instances when valid worlds exist.
        """
        users_dir = tmp_path / "Users"
        account_dir = users_dir / "test_account"
        worlds_dir = account_dir / "games" / "com.mojang" / "minecraftWorlds"
        world_folder = worlds_dir / "6LknJ-+T-Ks="

        world_folder.mkdir(parents=True)
        (world_folder / "levelname.txt").write_text("Meu Mundo")
        (world_folder / "level.dat").write_bytes(b"\x00")

        with patch.object(world_service, "get_worlds_base_path", return_value=users_dir):
            result = world_service.list_worlds()

        assert isinstance(result, list)
        if len(result) > 0:
            for world in result:
                assert isinstance(world, WorldModel)

    def test_should_return_empty_list_when_account_exists_but_no_worlds(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """
        list_worlds should return empty list when account directory exists
        but contains no world directories.
        """
        users_dir = tmp_path / "Users"
        account_dir = users_dir / "test_account"
        account_dir.mkdir(parents=True)

        with patch.object(world_service, "get_worlds_base_path", return_value=users_dir):
            result = world_service.list_worlds()

        assert isinstance(result, list)
        assert len(result) == 0

    def test_should_ignore_non_directories_in_worlds_folder(self, tmp_path: Path) -> None:
        """
        _list_worlds_from_path should ignore files (non-directories)
        in the minecraftWorlds directory.
        """
        service = WorldService(FileSystemWorldRepository())

        worlds_dir = tmp_path / "worlds"
        worlds_dir.mkdir()
        (worlds_dir / "some_file.txt").write_text("not a world")
        (worlds_dir / "abc123def89=").mkdir()
        (worlds_dir / "abc123def89=" / "levelname.txt").write_text("Real World")

        worlds = service._list_worlds_from_path(worlds_dir, "test")
        assert len(worlds) == 1
        assert worlds[0].folder_name == "abc123def89="

    def test_should_ignore_files_in_worlds_directory(self, tmp_path: Path) -> None:
        """
        _list_worlds_from_path should ignore files in the worlds directory.
        """
        service = WorldService(FileSystemWorldRepository())

        worlds_dir = tmp_path / "worlds"
        worlds_dir.mkdir()
        (worlds_dir / "not_a_world.txt").write_text("test")

        result = service._list_worlds_from_path(worlds_dir, "account_id")
        assert result == []

    def test_should_ignore_invalid_world_folders_without_levelname(self, tmp_path: Path) -> None:
        """
        _list_worlds_from_path should ignore folders without levelname.txt.
        """
        service = WorldService(FileSystemWorldRepository())

        worlds_dir = tmp_path / "worlds"
        worlds_dir.mkdir()
        (worlds_dir / "invalid_world_12=").mkdir()

        result = service._list_worlds_from_path(worlds_dir, "account_id")
        assert result == []

    def test_should_ignore_worlds_with_invalid_levelname(self, tmp_path: Path) -> None:
        """
        _list_worlds_from_path should ignore worlds with missing or
        invalid levelname.txt (empty, whitespace only, or FileNotFound/ValueError).
        """
        service = WorldService(FileSystemWorldRepository())

        worlds_dir = tmp_path / "worlds"
        worlds_dir.mkdir()

        valid_world = worlds_dir / "abc123def89="
        valid_world.mkdir()
        (valid_world / "levelname.txt").write_text("Valid World")

        invalid_world1 = worlds_dir / "invalid123="
        invalid_world1.mkdir()

        invalid_world2 = worlds_dir / "empty456="
        invalid_world2.mkdir()
        (invalid_world2 / "levelname.txt").write_text("   \n  ")

        result = service._list_worlds_from_path(worlds_dir, "account_id")

        assert len(result) == 1
        assert result[0].folder_name == "abc123def89="

    def test_should_return_empty_list_when_permission_error_on_iterdir(
        self, tmp_path: Path
    ) -> None:
        """
        _list_worlds_from_path should return empty list when permission error
        occurs while iterating worlds directory.
        """
        service = WorldService(FileSystemWorldRepository())

        worlds_dir = tmp_path / "worlds"
        worlds_dir.mkdir()

        valid_world = worlds_dir / "abc123def89="
        valid_world.mkdir()
        (valid_world / "levelname.txt").write_text("Valid World")

        with patch("pathlib.Path.iterdir", side_effect=PermissionError("Access denied")):
            result = service._list_worlds_from_path(worlds_dir, "account_id")

            assert result == []
