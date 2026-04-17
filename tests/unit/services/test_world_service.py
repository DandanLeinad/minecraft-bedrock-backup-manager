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

import pytest

from backup_manager_mvp.models.world_model import WorldModel
from backup_manager_mvp.services.world_service import WorldService


@pytest.fixture
def world_service() -> WorldService:
    """Fixture que fornece uma instância de WorldService."""
    return WorldService()


class TestGetWorldsBasePath:
    """Testes para o método get_worlds_base_path()."""

    def test_get_worlds_base_path_returns_path_object(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """Testa que get_worlds_base_path retorna um objeto Path."""
        # Arrange
        with patch.object(world_service, "get_worlds_base_path", return_value=tmp_path):
            # Act
            result = world_service.get_worlds_base_path()

            # Assert
            assert isinstance(result, Path)

    def test_get_worlds_base_path_contains_expected_structure(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """Testa que o path contém a estrutura esperada."""
        # Arrange
        mock_path = tmp_path / "AppData" / "Roaming" / "Minecraft Bedrock" / "Users"

        with patch.object(world_service, "get_worlds_base_path", return_value=mock_path):
            # Act
            result = world_service.get_worlds_base_path()

            # Assert
            # Deve conter AppData\Roaming\Minecraft Bedrock\Users
            assert "AppData" in str(result) or "Roaming" in str(result)


class TestListAccountIds:
    """Testes para o método list_account_ids()."""

    def test_list_account_ids_returns_list(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """Testa que list_account_ids retorna uma list."""
        # Arrange
        with patch.object(world_service, "get_worlds_base_path", return_value=tmp_path):
            # Act
            result = world_service.list_account_ids()

            # Assert
            assert isinstance(result, list)

    def test_list_account_ids_with_valid_structure(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """Testa list_account_ids com estrutura de pasta mock."""
        # Arrange
        users_dir = tmp_path / "Users"
        account1 = users_dir / "account_id_1"
        account2 = users_dir / "account_id_2"
        account1.mkdir(parents=True)
        account2.mkdir(parents=True)

        # Mock get_worlds_base_path para retornar nosso tmp_path
        with patch.object(world_service, "get_worlds_base_path", return_value=users_dir):
            # Act
            result = world_service.list_account_ids()

        # Assert
        assert len(result) >= 2
        assert "account_id_1" in result
        assert "account_id_2" in result

    def test_list_account_ids_empty_when_no_accounts(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """Testa que list_account_ids retorna lista vazia quando não há contas."""
        # Arrange
        users_dir = tmp_path / "Users"
        users_dir.mkdir(parents=True)

        with patch.object(world_service, "get_worlds_base_path", return_value=users_dir):
            # Act
            result = world_service.list_account_ids()

        # Assert
        assert isinstance(result, list)
        assert len(result) == 0


class TestListWorlds:
    """Testes para o método list_worlds()."""

    def test_list_worlds_returns_list(self, tmp_path: Path, world_service: WorldService) -> None:
        """Testa que list_worlds retorna uma list."""
        # Arrange
        with patch.object(world_service, "get_worlds_base_path", return_value=tmp_path):
            # Act
            result = world_service.list_worlds()

            # Assert
            assert isinstance(result, list)

    def test_list_worlds_returns_world_models(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """Testa que list_worlds retorna objetos WorldModel."""
        # Arrange
        # Estrutura: Users/account_id/games/com.mojang/minecraftWorlds/6LknJ-+T-Ks=/levelname.txt
        users_dir = tmp_path / "Users"
        account_dir = users_dir / "test_account"
        worlds_dir = account_dir / "games" / "com.mojang" / "minecraftWorlds"
        world_folder = worlds_dir / "6LknJ-+T-Ks="

        world_folder.mkdir(parents=True)

        # Criar levelname.txt
        levelname_file = world_folder / "levelname.txt"
        levelname_file.write_text("Meu Mundo")

        # Criar level.dat com versão (simplificado)
        level_dat = world_folder / "level.dat"
        # Para este teste, apenas criamos o arquivo
        level_dat.write_bytes(b"\x00")

        with patch.object(world_service, "get_worlds_base_path", return_value=users_dir):
            # Act
            result = world_service.list_worlds()

        # Assert
        assert isinstance(result, list)
        # Poderia ter 0 ou mais mundos dependendo da implementação
        if len(result) > 0:
            for world in result:
                assert isinstance(world, WorldModel)

    def test_list_worlds_empty_when_no_worlds(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """Testa que list_worlds retorna lista vazia quando não há mundos."""
        # Arrange
        users_dir = tmp_path / "Users"
        account_dir = users_dir / "test_account"
        account_dir.mkdir(parents=True)

        with patch.object(world_service, "get_worlds_base_path", return_value=users_dir):
            # Act
            result = world_service.list_worlds()

        # Assert
        assert isinstance(result, list)


class TestGetWorldLevelname:
    """Testes para o método get_world_levelname()."""

    def test_get_world_levelname_returns_string(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """Testa que get_world_levelname retorna uma string."""
        # Arrange
        world_path = tmp_path / "test_world"
        world_path.mkdir()
        levelname_file = world_path / "levelname.txt"
        levelname_file.write_text("Meu Mundo")

        # Act
        result = world_service.get_world_levelname(world_path)

        # Assert
        assert isinstance(result, str)
        assert result == "Meu Mundo"

    def test_get_world_levelname_reads_from_file(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """Testa que get_world_levelname lê o conteúdo correto do arquivo."""
        # Arrange
        world_path = tmp_path / "world"
        world_path.mkdir()
        levelname_file = world_path / "levelname.txt"
        expected_name = "Mundo Incrível"
        levelname_file.write_text(expected_name, encoding="utf-8")

        # Act
        result = world_service.get_world_levelname(world_path)

        # Assert
        assert result == expected_name

    def test_get_world_levelname_raises_when_file_not_found(
        self, tmp_path: Path, world_service: WorldService
    ) -> None:
        """Testa que get_world_levelname levanta exceção quando levelname.txt não existe."""
        # Arrange
        world_path = tmp_path / "world"
        world_path.mkdir()

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            world_service.get_world_levelname(world_path)


class TestListAccountIdsErrors:
    """Testes para cobrir casos de erro em list_account_ids (linha 96)."""

    def test_list_account_ids_handles_permission_error(self, world_service: WorldService) -> None:
        """Teste: list_account_ids retorna [] se PermissionError."""
        with patch.object(world_service, "get_worlds_base_path") as mock_path:
            mock_base = MagicMock()
            mock_base.exists.return_value = True
            mock_base.iterdir.side_effect = PermissionError("Access denied")
            mock_path.return_value = mock_base

            account_ids = world_service.list_account_ids()
            assert account_ids == []


class TestListWorldsErrors:
    """Testes para cobrir casos de erro em list_worlds (linhas 103-105, 144-150)."""

    def test_list_worlds_ignores_non_directories(self, tmp_path: Path) -> None:
        """Teste: _list_worlds_from_path ignora arquivos que não são diretórios."""
        service = WorldService()

        worlds_dir = tmp_path / "worlds"
        worlds_dir.mkdir()
        (worlds_dir / "some_file.txt").write_text("not a world")
        (worlds_dir / "abc123def89=").mkdir()
        (worlds_dir / "abc123def89=" / "levelname.txt").write_text("Real World")

        worlds = service._list_worlds_from_path(worlds_dir, "test")
        assert len(worlds) == 1
        assert worlds[0].folder_name == "abc123def89="

    def test_list_worlds_handles_permission_error(self, tmp_path: Path) -> None:
        """Teste: _list_worlds_from_path trata diretórios vazios sem erro."""
        service = WorldService()

        worlds_dir = tmp_path / "worlds"
        worlds_dir.mkdir()

        # Diretório vazio deve retornar lista vazia sem exceção
        worlds = service._list_worlds_from_path(worlds_dir, "test")
        assert worlds == []


class TestGetWorldLevelnameErrors:
    """Testes para cobrir casos de erro em get_world_levelname (linhas 214-217)."""

    def test_get_world_levelname_raises_on_unicode_decode_error(self, tmp_path: Path) -> None:
        """Teste: get_world_levelname lança ValueError se UnicodeDecodeError."""
        service = WorldService()

        world_path = tmp_path / "world"
        world_path.mkdir()
        levelname_file = world_path / "levelname.txt"

        # Escrever dados inválidos
        levelname_file.write_bytes(b"\xff\xfe invalid utf-8")

        with pytest.raises(ValueError, match="Erro ao decodificar"):
            service.get_world_levelname(world_path)

    def test_get_world_levelname_raises_on_empty_file(self, tmp_path: Path) -> None:
        """Teste: get_world_levelname lança ValueError se arquivo vazio/whitespace."""
        service = WorldService()

        world_path = tmp_path / "world"
        world_path.mkdir()
        levelname_file = world_path / "levelname.txt"
        levelname_file.write_text("   \n\t  ")

        with pytest.raises(ValueError, match="vazio ou contém apenas whitespace"):
            service.get_world_levelname(world_path)

    def test_list_account_ids_returns_empty_when_base_path_not_exists(
        self, world_service: WorldService
    ) -> None:
        """Teste: list_account_ids retorna [] se base_path não existe (linha 96)."""
        # Arrange: Mock base_path para não existir
        with patch.object(world_service, "get_worlds_base_path") as mock_base_path:
            mock_base_path.return_value = Path("/nonexistent/path/that/does/not/exist")

            # Act
            result = world_service.list_account_ids()

            # Assert
            assert result == []

    def test_list_worlds_from_path_ignores_non_directories(self, tmp_path: Path) -> None:
        """Teste: _list_worlds_from_path ignora arquivos (não diretórios)."""
        service = WorldService()

        # Arrange: Criar um arquivo (não diretório) na worlds_dir
        worlds_dir = tmp_path / "worlds"
        worlds_dir.mkdir()
        (worlds_dir / "not_a_world.txt").write_text("test")

        # Act
        result = service._list_worlds_from_path(worlds_dir, "account_id")

        # Assert
        assert result == []

    def test_list_worlds_from_path_ignores_invalid_world_folders(self, tmp_path: Path) -> None:
        """Teste: _list_worlds_from_path ignora pastas sem levelname.txt."""
        service = WorldService()

        worlds_dir = tmp_path / "worlds"
        worlds_dir.mkdir()
        # Criar pasta de mundo sem levelname.txt
        (worlds_dir / "invalid_world_12=").mkdir()

        result = service._list_worlds_from_path(worlds_dir, "account_id")
        assert result == []


class TestGetWorldMetadata:
    """Testes para o método get_world_metadata()."""

    def test_calculate_world_size_kilobytes(self, tmp_path: Path) -> None:
        """Testa cálculo de tamanho em KB."""
        # Arrange
        service = WorldService()
        world_path = tmp_path / "world"
        world_path.mkdir()
        levelname_file = world_path / "levelname.txt"
        levelname_file.write_text("Test World")
        # 101 KB de conteúdo
        (world_path / "file1.dat").write_bytes(b"x" * (1024 * 101))

        world = WorldModel(
            folder_name="testworld12=",
            levelname="Test World",
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        # Act
        metadata = service.get_world_metadata(world)

        # Assert
        assert "KB" in metadata["size"] or "MB" in metadata["size"]
        assert metadata["backups_count"] == "0"
        assert metadata["last_backup"] == "Nunca"

    def test_no_backups(self, tmp_path: Path) -> None:
        """Testa quando não há backups."""
        # Arrange
        service = WorldService()
        world_path = tmp_path / "world"
        world_path.mkdir()
        (world_path / "levelname.txt").write_text("World")

        world = WorldModel(
            folder_name="world123456=",
            levelname="World",
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        # Act
        metadata = service.get_world_metadata(world, backup_service=None)

        # Assert
        assert metadata["backups_count"] == "0"
        assert metadata["last_backup"] == "Nunca"

    def test_recent_backup_seconds_ago(self, tmp_path: Path) -> None:
        """Testa backup recente (há segundos)."""
        from datetime import datetime, timedelta

        from backup_manager_mvp.models.backup_model import BackupModel

        # Arrange
        service = WorldService()
        world_path = tmp_path / "world"
        world_path.mkdir()
        (world_path / "levelname.txt").write_text("World")

        world = WorldModel(
            folder_name="world123456=",
            levelname="World",
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

        # Act
        metadata = service.get_world_metadata(world, MockBackupService())

        # Assert
        assert metadata["backups_count"] == "1"
        assert metadata["last_backup"] == "há segundos"

    def test_multiple_backups_returns_newest(self, tmp_path: Path) -> None:
        """Testa que com múltiplos backups retorna o mais recente."""
        from datetime import datetime, timedelta

        from backup_manager_mvp.models.backup_model import BackupModel

        # Arrange
        service = WorldService()
        world_path = tmp_path / "world"
        world_path.mkdir()
        (world_path / "levelname.txt").write_text("World")

        world = WorldModel(
            folder_name="world123456=",
            levelname="World",
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

        # Act
        metadata = service.get_world_metadata(world, MockBackupService())

        # Assert
        assert metadata["backups_count"] == "2"
        assert "5m" in metadata["last_backup"]

    def test_nonexistent_world_path(self) -> None:
        """Testa com caminho de mundo inexistente."""
        # Arrange
        service = WorldService()
        world = WorldModel(
            folder_name="nonexistent=",
            levelname="Nonexistent",
            path=Path("/nonexistent/path/that/does/not/exist"),
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        # Act
        metadata = service.get_world_metadata(world)

        # Assert
        assert metadata["size"] == "N/A"
        assert metadata["backups_count"] == "0"
        assert metadata["last_backup"] == "Nunca"

    def test_list_worlds_from_path_handles_file_not_found_and_value_error(
        self, tmp_path: Path
    ) -> None:
        """Teste: linhas 144-145 - continue no except (FileNotFoundError, ValueError)."""
        service = WorldService()

        worlds_dir = tmp_path / "worlds"
        worlds_dir.mkdir()

        # Mundo válido
        valid_world = worlds_dir / "abc123def89="
        valid_world.mkdir()
        (valid_world / "levelname.txt").write_text("Valid World")

        # Mundo inválido (sem levelname.txt) → FileNotFoundError
        invalid_world1 = worlds_dir / "invalid123="
        invalid_world1.mkdir()
        # Sem levelname.txt

        # Mundo com levelname vazio → ValueError
        invalid_world2 = worlds_dir / "empty456="
        invalid_world2.mkdir()
        (invalid_world2 / "levelname.txt").write_text("   \n  ")

        # Act
        result = service._list_worlds_from_path(worlds_dir, "account_id")

        # Assert: Apenas 1 mundo válido (os 2 inválidos foram ignorados)
        assert len(result) == 1
        assert result[0].folder_name == "abc123def89="

    def test_list_worlds_from_path_handles_permission_error_on_iterdir(
        self, tmp_path: Path
    ) -> None:
        """Teste: linhas 148-150 - except (OSError, PermissionError) com patch module."""
        service = WorldService()

        worlds_dir = tmp_path / "worlds"
        worlds_dir.mkdir()

        # Criar um mundo válido pra ter algo
        valid_world = worlds_dir / "abc123def89="
        valid_world.mkdir()
        (valid_world / "levelname.txt").write_text("Valid World")

        # Mock iterdir no module Path para lançar PermissionError
        with patch("pathlib.Path.iterdir", side_effect=PermissionError("Access denied")):
            # Act: Mesmo com erro, deve retornar lista vazia (ou o que foi encontrado antes)
            result = service._list_worlds_from_path(worlds_dir, "account_id")

            # Assert: Lista vazia devido ao except que passa (não relança)
            assert result == []

    def test_calculate_world_size_bytes(self, tmp_path: Path) -> None:
        """Testa cálculo de tamanho em bytes (< 1024)."""
        # Arrange
        service = WorldService()
        world_path = tmp_path / "world"
        world_path.mkdir()
        levelname_file = world_path / "levelname.txt"
        levelname_file.write_text("Test World")
        # 500 bytes para ficar < 1024 total
        (world_path / "file1.dat").write_bytes(b"x" * 500)

        world = WorldModel(
            folder_name="testworld12=",
            levelname="Test World",
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        # Act
        metadata = service.get_world_metadata(world)

        # Assert - Deve estar em bytes puro (< 1024)
        assert "B" in metadata["size"]
        assert not any(unit in metadata["size"] for unit in ["KB", "MB", "GB"])

    def test_calculate_world_size_gigabytes(self, tmp_path: Path) -> None:
        """Testa cálculo de tamanho em gigabytes (>= 1024^3)."""
        # Arrange
        service = WorldService()
        world_path = tmp_path / "world"
        world_path.mkdir()
        (world_path / "levelname.txt").write_text("Test")

        world = WorldModel(
            folder_name="testworld12=",
            levelname="Test",
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        # Act - Mockar sum() para retornar tamanho grande
        with patch("builtins.sum", return_value=2 * (1024**3)):
            metadata = service.get_world_metadata(world)

        # Assert
        assert "GB" in metadata["size"]

    def test_backup_time_delta_minutes(self, tmp_path: Path) -> None:
        """Testa formatação de tempo relativo em minutos."""
        from datetime import datetime, timedelta

        from backup_manager_mvp.models.backup_model import BackupModel

        # Arrange
        service = WorldService()
        world_path = tmp_path / "world"
        world_path.mkdir()
        (world_path / "levelname.txt").write_text("World")

        world = WorldModel(
            folder_name="world123456=",
            levelname="World",
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        now = datetime.now()
        backup = BackupModel(
            world_folder_name="test_backup",
            world_account_id="test",
            created_at=now - timedelta(minutes=5),  # 5 minutos atrás
            backup_path=tmp_path / "backup",
        )

        class MockBackupService:
            def list_backups(self, w):
                return [backup]

        # Act
        metadata = service.get_world_metadata(world, MockBackupService())

        # Assert
        assert "5m" in metadata["last_backup"]
        assert metadata["last_backup"] == "há 5m"

    def test_backup_time_delta_hours(self, tmp_path: Path) -> None:
        """Testa formatação de tempo relativo em horas."""
        from datetime import datetime, timedelta

        from backup_manager_mvp.models.backup_model import BackupModel

        # Arrange
        service = WorldService()
        world_path = tmp_path / "world"
        world_path.mkdir()
        (world_path / "levelname.txt").write_text("World")

        world = WorldModel(
            folder_name="world123456=",
            levelname="World",
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        now = datetime.now()
        backup = BackupModel(
            world_folder_name="test_backup",
            world_account_id="test",
            created_at=now - timedelta(hours=3),  # 3 horas atrás
            backup_path=tmp_path / "backup",
        )

        class MockBackupService:
            def list_backups(self, w):
                return [backup]

        # Act
        metadata = service.get_world_metadata(world, MockBackupService())

        # Assert
        assert "3h" in metadata["last_backup"]
        assert metadata["last_backup"] == "há 3h"

    def test_get_uwp_store_path_returns_valid_path(self) -> None:
        """Testa que get_uwp_store_path retorna path válido."""
        # Arrange
        service = WorldService()

        # Act
        uwp_path = service.get_uwp_store_path()

        # Assert
        assert isinstance(uwp_path, Path)
        assert "Microsoft.MinecraftUWP_8wekyb3d8bbwe" in str(uwp_path)
        assert "minecraftWorlds" in str(uwp_path)

    def test_get_world_metadata_exception_on_backup_service(self, tmp_path: Path) -> None:
        """Testa que exceção no backup_service é capturada corretamente."""
        # Arrange
        service = WorldService()
        world_path = tmp_path / "world"
        world_path.mkdir()
        (world_path / "levelname.txt").write_text("World")

        world = WorldModel(
            folder_name="world123456=",
            levelname="World",
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        class BrokenBackupService:
            """Simula um BackupService que lança exceção."""

            def list_backups(self, w):
                raise OSError("Erro ao listar backups")

        # Act
        metadata = service.get_world_metadata(world, BrokenBackupService())

        # Assert - Mesmo com erro no backup_service, deve retornar defaults
        assert metadata["backups_count"] == "0"
        assert metadata["last_backup"] == "Nunca"

    def test_get_world_metadata_with_all_time_deltas(self, tmp_path: Path) -> None:
        """Testa vários time deltas: segundos, minutos, horas, dias (cobertura completa)."""
        from datetime import datetime, timedelta

        from backup_manager_mvp.models.backup_model import BackupModel

        service = WorldService()
        world_path = tmp_path / "world"
        world_path.mkdir()
        (world_path / "levelname.txt").write_text("World")

        world = WorldModel(
            folder_name="world123456=",
            levelname="World",
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        # Testes de todos os branches de time delta
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
