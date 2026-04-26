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

from pathlib import Path
from unittest.mock import MagicMock, patch

from backup_manager_mvp.core.models.world_model import WorldModel
from backup_manager_mvp.core.services.world_service import WorldService
from backup_manager_mvp.infra.repository import FileSystemWorldRepository


class TestGetWorldsBasePath:
    def test_get_worlds_base_path_returns_path_object(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        with patch.object(world_service, "get_worlds_base_path", return_value=tmp_path):
            result = world_service.get_worlds_base_path()

        assert isinstance(result, Path)

    def test_get_worlds_base_path_contains_expected_structure(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        mock_path = tmp_path / "AppData" / "Roaming" / "Minecraft Bedrock" / "Users"

        with patch.object(world_service, "get_worlds_base_path", return_value=mock_path):
            result = world_service.get_worlds_base_path()

        assert "AppData" in str(result) or "Roaming" in str(result)


class TestListAccountIds:
    def test_list_account_ids_returns_list(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        with patch.object(world_service, "get_worlds_base_path", return_value=tmp_path):
            result = world_service.list_account_ids()

        assert isinstance(result, list)

    def test_list_account_ids_with_valid_structure(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
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

    def test_list_account_ids_empty_when_no_accounts(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        users_dir = tmp_path / "Users"
        users_dir.mkdir(parents=True)

        with patch.object(world_service, "get_worlds_base_path", return_value=users_dir):
            result = world_service.list_account_ids()

        assert isinstance(result, list)
        assert len(result) == 0

    def test_list_account_ids_handles_permission_error(self, world_service: WorldService) -> None:
        with patch.object(world_service, "get_worlds_base_path") as mock_path:
            mock_base = MagicMock()
            mock_base.exists.return_value = True
            mock_base.iterdir.side_effect = PermissionError("Access denied")
            mock_path.return_value = mock_base

            account_ids = world_service.list_account_ids()
            assert account_ids == []

    def test_list_account_ids_returns_empty_when_base_path_not_exists(
        self, world_service: WorldService
    ) -> None:
        with patch.object(world_service, "get_worlds_base_path") as mock_base_path:
            mock_base_path.return_value = Path("/nonexistent/path/that/does/not/exist")

            result = world_service.list_account_ids()

            assert result == []


class TestListWorlds:
    def test_list_worlds_returns_list(self, tmp_path: Path, world_service: WorldService) -> None:
        with patch.object(world_service, "get_worlds_base_path", return_value=tmp_path):
            result = world_service.list_worlds()

        assert isinstance(result, list)

    def test_list_worlds_returns_world_models(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
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

    def test_list_worlds_empty_when_no_worlds(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        users_dir = tmp_path / "Users"
        account_dir = users_dir / "test_account"
        account_dir.mkdir(parents=True)

        with patch.object(world_service, "get_worlds_base_path", return_value=users_dir):
            result = world_service.list_worlds()

        assert isinstance(result, list)

    def test_list_worlds_ignores_non_directories(self, tmp_path: Path) -> None:
        service = WorldService(FileSystemWorldRepository())

        worlds_dir = tmp_path / "worlds"
        worlds_dir.mkdir()
        (worlds_dir / "some_file.txt").write_text("not a world")
        (worlds_dir / "abc123def89=").mkdir()
        (worlds_dir / "abc123def89=" / "levelname.txt").write_text("Real World")

        worlds = service._list_worlds_from_path(worlds_dir, "test")
        assert len(worlds) == 1
        assert worlds[0].folder_name == "abc123def89="

    def test_list_worlds_from_path_ignores_files(self, tmp_path: Path) -> None:
        service = WorldService(FileSystemWorldRepository())

        worlds_dir = tmp_path / "worlds"
        worlds_dir.mkdir()
        (worlds_dir / "not_a_world.txt").write_text("test")

        result = service._list_worlds_from_path(worlds_dir, "account_id")
        assert result == []

    def test_list_worlds_ignores_invalid_world_folders(self, tmp_path: Path) -> None:
        service = WorldService(FileSystemWorldRepository())

        worlds_dir = tmp_path / "worlds"
        worlds_dir.mkdir()
        (worlds_dir / "invalid_world_12=").mkdir()

        result = service._list_worlds_from_path(worlds_dir, "account_id")
        assert result == []

    def test_list_worlds_from_path_handles_file_not_found_and_value_error(
        self, tmp_path: Path
    ) -> None:
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

    def test_list_worlds_from_path_handles_permission_error_on_iterdir(
        self, tmp_path: Path
    ) -> None:
        service = WorldService(FileSystemWorldRepository())

        worlds_dir = tmp_path / "worlds"
        worlds_dir.mkdir()

        valid_world = worlds_dir / "abc123def89="
        valid_world.mkdir()
        (valid_world / "levelname.txt").write_text("Valid World")

        with patch("pathlib.Path.iterdir", side_effect=PermissionError("Access denied")):
            result = service._list_worlds_from_path(worlds_dir, "account_id")

            assert result == []
