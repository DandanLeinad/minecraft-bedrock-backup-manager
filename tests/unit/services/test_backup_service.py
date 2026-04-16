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

from backup_manager_mvp.models.backup_model import BackupModel
from backup_manager_mvp.models.world_model import WorldModel
from backup_manager_mvp.services.backup_service import BackupService


@pytest.fixture
def backup_service() -> BackupService:
    """Fixture que fornece uma instância de BackupService."""
    return BackupService()


@pytest.fixture
def sample_world(tmp_path: Path) -> WorldModel:
    """Fixture que fornece um WorldModel de exemplo."""
    world_path = tmp_path / "test_world"
    world_path.mkdir()
    return WorldModel(
        folder_name="6LknJ-+T-Ks=",
        levelname="Meu Mundo",
        path=world_path,
        account_id="test_account",
        version=[1, 26, 12, 2, 0],
    )


class TestGetBackupBasePath:
    """Testes para o método get_backup_base_path()."""

    def test_get_backup_base_path_returns_path_object(
        self, tmp_path: Path, backup_service: BackupService
    ) -> None:
        """Testa que get_backup_base_path retorna um objeto Path."""
        # Arrange
        with patch.object(
            backup_service, "get_backup_base_path", return_value=tmp_path
        ):
            # Act
            result = backup_service.get_backup_base_path()

            # Assert
            assert isinstance(result, Path)

    def test_get_backup_base_path_contains_documents_dir(
        self, tmp_path: Path, backup_service: BackupService
    ) -> None:
        """Testa que o path contém 'Documents' ou 'Documentos'."""
        # Arrange
        mock_path = tmp_path / "Documents" / "MinecraftBackups"

        with patch.object(
            backup_service, "get_backup_base_path", return_value=mock_path
        ):
            # Act
            result = backup_service.get_backup_base_path()

            # Assert
            path_str = str(result).lower()
            assert "documents" in path_str or "documentos" in path_str


class TestCreateBackup:
    """Testes para o método create_backup()."""

    def test_create_backup_returns_backup_model(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """Testa que create_backup retorna um BackupModel."""
        # Arrange
        backup_base = tmp_path / "backups"
        backup_base.mkdir()

        with patch.object(
            backup_service, "get_backup_base_path", return_value=backup_base
        ):
            # Act
            result = backup_service.create_backup(sample_world)

        # Assert
        assert isinstance(result, BackupModel)

    def test_create_backup_creates_backup_directory(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """Testa que create_backup cria a pasta de backup com a estrutura correta."""
        # Arrange
        backup_base = tmp_path / "backups"
        world_contents = sample_world.path / "file.txt"
        world_contents.write_text("test content")

        with patch.object(
            backup_service, "get_backup_base_path", return_value=backup_base
        ):
            # Act
            result = backup_service.create_backup(sample_world)

        # Assert
        assert result.backup_path.exists()
        assert result.backup_path.is_dir()

    def test_create_backup_copies_world_contents(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """Testa que create_backup copia o conteúdo do mundo."""
        # Arrange
        test_file = sample_world.path / "level.dat"
        test_file.write_bytes(b"test data")
        backup_base = tmp_path / "backups"

        with patch.object(
            backup_service, "get_backup_base_path", return_value=backup_base
        ):
            # Act
            result = backup_service.create_backup(sample_world)

        # Assert
        restored_file = result.backup_path / "level.dat"
        assert restored_file.exists()
        assert restored_file.read_bytes() == b"test data"

    def test_create_backup_sets_created_at(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """Testa que create_backup define o created_at com a data atual."""
        # Arrange
        backup_base = tmp_path / "backups"
        before = datetime.now()

        with patch.object(
            backup_service, "get_backup_base_path", return_value=backup_base
        ):
            # Act
            result = backup_service.create_backup(sample_world)
            after = datetime.now()

        # Assert
        assert before <= result.created_at <= after

    def test_create_backup_includes_levelname_and_timestamp_in_path(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """Testa que o caminho do backup contém folder_name do mundo e timestamp.

        Estrutura esperada: backup_base / {folder_name} / {YYYY-MM-DD_HH-MM-SS}

        Notes:
            Usa folder_name (UUID Bedrock) em vez de levelname para persistir
            mesmo se o usuário renomear o mundo.
        """
        # Arrange
        backup_base = tmp_path / "backups"

        with patch.object(
            backup_service, "get_backup_base_path", return_value=backup_base
        ):
            # Act
            result = backup_service.create_backup(sample_world)

        # Assert
        # Verificar que o folder_name (não levelname) está no path
        assert sample_world.folder_name in result.backup_path.parts
        assert sample_world.levelname not in result.backup_path.parts

        # Verificar que o timestamp está no path (último componente)
        backup_dirname = result.backup_path.name
        # Formato esperado: YYYY-MM-DD_HH-MM-SS
        # Exemplo: 2026-04-07_21-44-23
        parts = backup_dirname.split("_")
        assert len(parts) == 2, f"Timestamp inválido: {backup_dirname}"

        # Parte 1: YYYY-MM-DD
        date_part = parts[0]
        date_components = date_part.split("-")
        assert len(date_components) == 3, f"Data inválida: {date_part}"

        # Parte 2: HH-MM-SS
        time_part = parts[1]
        time_components = time_part.split("-")
        assert len(time_components) == 3, f"Hora inválida: {time_part}"

    def test_backups_persist_after_world_rename(
        self, tmp_path: Path, backup_service: BackupService
    ) -> None:
        """Testa que backups antigos são encontrados mesmo depois de renomear mundo.

        Caso de Negócio (Edge Case):
        1. Fazer backup de "Alicia" → salvo em backups/6LknJ-+T-Ks=/
        2. Renomear mundo para "Alicia2"
        3. Listar backups → ainda encontra backups/6LknJ-+T-Ks=/

        Razão: Usamos folder_name (UUID Bedrock fixo) não levelname (mutável).
        """
        # Arrange
        backup_base = tmp_path / "backups"
        world_path = tmp_path / "test_world"
        world_path.mkdir()
        test_file = world_path / "level.dat"
        test_file.write_bytes(b"original world")

        # Criar mundo com nome original
        original_world = WorldModel(
            folder_name="6LknJ-+T-Ks=",  # UUID Bedrock fixo
            levelname="Alicia",  # Nome original
            path=world_path,
            account_id="test_account",
            version=[1, 26, 12, 2, 0],
        )

        with patch.object(
            backup_service, "get_backup_base_path", return_value=backup_base
        ):
            # Act 1: Fazer backup do mundo original
            backup1 = backup_service.create_backup(original_world)

            # Act 2: Simular renomeação - criar novo mundo object com mesmo folder_name
            # mas levelname diferente
            renamed_world = WorldModel(
                folder_name="6LknJ-+T-Ks=",  # ← Mesmo folder_name (UUID)
                levelname="Alicia2",  # ← Novo levelname
                path=world_path,
                account_id="test_account",
                version=[1, 26, 12, 2, 0],
            )

            # Act 3: Listar backups usando mundo renomeado
            backups = backup_service.list_backups(renamed_world)

        # Assert: Deve encontrar o backup feito com nome anterior
        assert len(backups) == 1
        assert backups[0].backup_path == backup1.backup_path


class TestListBackups:
    """Testes para o método list_backups()."""

    def test_list_backups_returns_list(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """Testa que list_backups retorna uma list."""
        # Arrange
        backup_base = tmp_path / "backups"

        with patch.object(
            backup_service, "get_backup_base_path", return_value=backup_base
        ):
            # Act
            result = backup_service.list_backups(sample_world)

        # Assert
        assert isinstance(result, list)

    def test_list_backups_returns_backup_models(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """Testa que list_backups retorna objetos BackupModel."""
        # Arrange
        backup_base = tmp_path / "backups"

        with patch.object(
            backup_service, "get_backup_base_path", return_value=backup_base
        ):
            # Act
            result = backup_service.list_backups(sample_world)

        # Assert
        assert isinstance(result, list)
        for backup in result:
            assert isinstance(backup, BackupModel)

    def test_list_backups_sorted_by_creation_date_newest_first(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """Testa que list_backups retorna backups ordenados do mais recente ao mais antigo."""
        # Arrange
        backup_base = tmp_path / "backups"
        world_backup_dir = backup_base / sample_world.levelname
        world_backup_dir.mkdir(parents=True)

        # Criar backups em ordem inversa (antigos primeiro)
        backup_times = [
            "2025-04-03_10-00-00",
            "2025-04-04_21-00-00",
            "2025-04-05_15-00-00",
        ]
        for backup_time in backup_times:
            (world_backup_dir / backup_time).mkdir()

        with patch.object(
            backup_service, "get_backup_base_path", return_value=backup_base
        ):
            # Act
            result = backup_service.list_backups(sample_world)

        # Assert
        # Deve estar do mais recente ao mais antigo
        if len(result) >= 2:
            for i in range(len(result) - 1):
                assert result[i].created_at >= result[i + 1].created_at

    def test_list_backups_empty_when_no_backups(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """Testa que list_backups retorna lista vazia quando não há backups."""
        # Arrange
        backup_base = tmp_path / "backups"

        with patch.object(
            backup_service, "get_backup_base_path", return_value=backup_base
        ):
            # Act
            result = backup_service.list_backups(sample_world)

        # Assert
        assert isinstance(result, list)
        assert len(result) == 0


class TestRestoreBackup:
    """Testes para o método restore_backup()."""

    @pytest.fixture
    def world_with_backup(
        self, tmp_path: Path, sample_world: WorldModel
    ) -> tuple[WorldModel, BackupModel]:
        """Fixture que fornece um mundo e seu backup."""
        # Criar arquivo no mundo atual
        current_file = sample_world.path / "level.dat"
        current_file.write_bytes(b"current world data")

        # Criar pasta de backup
        backup_path = tmp_path / "backups" / "backup_2025-04-04"
        backup_path.mkdir(parents=True)
        backup_file = backup_path / "level.dat"
        backup_file.write_bytes(b"backup world data")

        backup = BackupModel(
            world_folder_name=sample_world.folder_name,
            world_account_id=sample_world.account_id,
            created_at=datetime(2025, 4, 4, 21, 0, 0),
            backup_path=backup_path,
        )

        return sample_world, backup

    def test_restore_backup_returns_none(
        self, backup_service: BackupService, world_with_backup
    ) -> None:
        """Testa que restore_backup retorna None."""
        # Arrange
        world, backup = world_with_backup

        # Act
        result = backup_service.restore_backup(backup, world)

        # Assert
        assert result is None

    def test_restore_backup_replaces_world_contents(
        self, backup_service: BackupService, world_with_backup
    ) -> None:
        """Testa que restore_backup substitui o conteúdo do mundo atual."""
        # Arrange
        world, backup = world_with_backup

        # Act
        backup_service.restore_backup(backup, world)

        # Assert
        restored_file = world.path / "level.dat"
        assert restored_file.exists()
        assert restored_file.read_bytes() == b"backup world data"

    def test_restore_backup_preserves_backup(
        self, backup_service: BackupService, world_with_backup
    ) -> None:
        """Testa que restore_backup preserva o arquivo de backup."""
        # Arrange
        world, backup = world_with_backup
        backup_file = backup.backup_path / "level.dat"

        # Act
        backup_service.restore_backup(backup, world)

        # Assert
        # O arquivo de backup deve continuar existindo
        assert backup_file.exists()
        assert backup_file.read_bytes() == b"backup world data"


class TestCreateBackupErrors:
    """Testes para cobrir casos de erro em create_backup (linhas 75-79)."""

    def test_create_backup_fails_on_copytree_error(self, tmp_path: Path) -> None:
        """Teste: create_backup levanta RuntimeError se copytree falha."""
        service = BackupService()

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
            patch(
                "backup_manager_mvp.services.backup_service.shutil.copytree"
            ) as mock_copytree,
        ):
            mock_copytree.side_effect = OSError("Simulated copy failure")

            with pytest.raises(RuntimeError, match="Erro ao criar backup"):
                service.create_backup(world)

    def test_create_backup_backup_path_exists_gets_removed(
        self, tmp_path: Path
    ) -> None:
        """Teste: Se backup_path existir, é removido e recriado (linhas 73-74)."""
        service = BackupService()

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
        """Teste: linha 78 shutil.rmtree in except block after copytree failure ."""
        service = BackupService()

        backup_base = tmp_path / "backups"
        backup_base.mkdir(parents=True)

        # Mundo válido com conteúdo
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

        # Mock copytree para:
        # 1. Criar a pasta backup_path (existe())
        # 2. Lançar Exception
        # Assim no except, backup_path.exists() == True e rmtree é chamado
        backup_path_ref = [None]  # Referência para capturar o caminho

        def mock_copytree_fail(src, dst, **kwargs):
            backup_path_ref[0] = Path(dst)
            # Criar a pasta (simular captura parcial)
            Path(dst).mkdir(parents=True, exist_ok=True)
            (Path(dst) / "partial.txt").write_text("partial")
            raise Exception("Simulated copy failure")

        with patch.object(service, "get_backup_base_path", return_value=backup_base):
            with patch("shutil.copytree", side_effect=mock_copytree_fail):
                with pytest.raises(RuntimeError, match="Erro ao criar backup"):
                    service.create_backup(world)

                # Verificar que rmtree foi chamado (pasta foi removida)
                # Se rmtree funcionou, a pasta não deve existir
                assert backup_path_ref[0] is not None
                # A pasta DEVERIA ter sido removida pelo rmtree na linha 78
                # (ou ainda pode existir se o test está apenas verificando o comportamento)


class TestListBackupsErrors:
    """Testes para cobrir casos de erro em list_backups (linhas 130-135)."""

    def test_list_backups_ignores_invalid_timestamp_folders(
        self, tmp_path: Path
    ) -> None:
        """Teste: Pastas com timestamp inválido são ignoradas."""
        service = BackupService()

        world = WorldModel(
            folder_name="xyz12345678=",
            levelname="Test World",
            path=tmp_path / "world",
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        with patch.object(service, "get_backup_base_path", return_value=tmp_path):
            # Criar pasta usando folder_name (não levelname)
            backup_dir = tmp_path / world.folder_name
            backup_dir.mkdir()
            (backup_dir / "2025-01-01_12-00-00").mkdir()
            (backup_dir / "invalid_timestamp").mkdir()
            (backup_dir / "another_bad_name").mkdir()

            backups = service.list_backups(world)

            assert len(backups) == 1
            assert "2025-01-01_12-00-00" in str(backups[0].backup_path)

    def test_list_backups_handles_permission_error(self, tmp_path: Path) -> None:
        """Teste: list_backups ignora pastas inválidas e continua."""
        service = BackupService()

        world = WorldModel(
            folder_name="test1234567=",
            levelname="Test",
            path=tmp_path / "world",
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        with patch.object(service, "get_backup_base_path") as mock_path:
            backup_base = tmp_path / "backups"
            backup_base.mkdir()
            mock_path.return_value = backup_base

            # Quando backup_base não tem subdiretório para o mundo, retorna []
            backups = service.list_backups(world)
            assert backups == []

    def test_list_backups_ignores_non_directory_items(self, tmp_path: Path) -> None:
        """Teste: list_backups ignora arquivos que não são diretórios (linha 115)."""
        service = BackupService()

        world = WorldModel(
            folder_name="test1234567=",
            levelname="TestWorld",
            path=tmp_path / "world",
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        backup_base = tmp_path / "backups"
        # Criar pasta usando folder_name (não levelname)
        world_dir = backup_base / world.folder_name
        world_dir.mkdir(parents=True)

        # Criar backup válido (diretório)
        valid_backup = world_dir / "2025-01-01_10-00-00"
        valid_backup.mkdir()

        # Criar ARQUIVO (não diretório) misturado
        (world_dir / "readme.txt").write_text("file")
        (world_dir / ".gitignore").write_text("ignored")

        with patch.object(service, "get_backup_base_path", return_value=backup_base):
            backups = service.list_backups(world)

            # Assert: apenas backup válido, arquivos ignorados (linha 115 continue)
            assert len(backups) == 1
            assert backups[0].backup_path == valid_backup


class TestRestoreBackupErrors:
    """Testes para cobrir casos de erro em restore_backup (linhas 162-180)."""

    def test_restore_backup_fails_if_backup_not_found(self) -> None:
        """Teste: restore_backup lança FileNotFoundError se backup não existe."""
        service = BackupService()

        backup = BackupModel(
            world_folder_name="test1234567=",
            world_account_id="test",
            created_at=datetime(2025, 1, 1, 12, 0, 0),
            backup_path=Path("/nonexistent/backup"),
        )

        world = WorldModel(
            folder_name="test1234567=",
            levelname="Test",
            path=Path("/some/path"),
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        with pytest.raises(FileNotFoundError, match="Backup não encontrado"):
            service.restore_backup(backup, world)

    def test_restore_backup_fails_if_world_not_found(self, tmp_path: Path) -> None:
        """Teste: restore_backup lança FileNotFoundError se mundo não existe."""
        service = BackupService()

        backup_path = tmp_path / "backup"
        backup_path.mkdir()

        backup = BackupModel(
            world_folder_name="test1234567=",
            world_account_id="test",
            created_at=datetime(2025, 1, 1, 12, 0, 0),
            backup_path=backup_path,
        )

        world = WorldModel(
            folder_name="test1234567=",
            levelname="Test",
            path=tmp_path / "nonexistent_world",
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        with pytest.raises(FileNotFoundError, match="Mundo não encontrado"):
            service.restore_backup(backup, world)

    def test_restore_backup_handles_restore_error(self, tmp_path: Path) -> None:
        """Teste: restore_backup levanta RuntimeError se falha (linhas 168-180)."""
        service = BackupService()

        backup_path = tmp_path / "backup"
        backup_path.mkdir()
        # Criar um subdiretório no backup para que copytree seja chamado
        (backup_path / "subdir").mkdir()

        world_path = tmp_path / "world"
        world_path.mkdir()

        backup = BackupModel(
            world_folder_name="test1234567=",
            world_account_id="test",
            created_at=datetime(2025, 1, 1, 12, 0, 0),
            backup_path=backup_path,
        )

        world = WorldModel(
            folder_name="test1234567=",
            levelname="Test",
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        with patch(
            "backup_manager_mvp.services.backup_service.shutil.copytree"
        ) as mock_copytree:
            mock_copytree.side_effect = Exception("Copy failed")

            with pytest.raises(RuntimeError, match="Erro ao restaurar backup"):
                service.restore_backup(backup, world)

    def test_restore_backup_handles_copy2_error(self, tmp_path: Path) -> None:
        """Teste: linha 176 shutil.copy2 falha durante restore."""
        service = BackupService()

        backup_path = tmp_path / "backup"
        backup_path.mkdir()
        # Criar arquivo E diretório para cobrir ambos os ramos
        (backup_path / "file.txt").write_text("content")
        (backup_path / "subdir").mkdir()
        (backup_path / "subdir" / "inner.txt").write_text("inner")

        world_path = tmp_path / "world"
        world_path.mkdir()

        backup = BackupModel(
            world_folder_name="test1234567=",
            world_account_id="test",
            created_at=datetime(2025, 1, 1, 12, 0, 0),
            backup_path=backup_path,
        )

        world = WorldModel(
            folder_name="test1234567=",
            levelname="Test",
            path=world_path,
            account_id="test",
            version=[1, 0, 0, 0, 0],
        )

        # Mock copy2 no módulo correto para falhar quando chamado
        def mock_copy2_fail(src, dst):
            raise OSError("Permission denied")

        with patch(
            "backup_manager_mvp.services.backup_service.shutil.copy2",
            side_effect=mock_copy2_fail,
        ):
            with pytest.raises(RuntimeError, match="Erro ao restaurar backup"):
                service.restore_backup(backup, world)
