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

"""Fixtures para testes de integração com filesystem real."""

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from backup_manager_mvp.core.models.world_model import WorldModel
from backup_manager_mvp.infra.repository import (
    FileSystemBackupRepository,
    FileSystemWorldRepository,
)


class TestFileSystemWorldRepository(FileSystemWorldRepository):
    """Repositório de teste que usa diretório temporário em vez do real."""

    def __init__(self, base_path: Path):
        self._test_base_path = base_path
        # Não chamar super().__init__() para evitar inicialização do pathlib real

    def get_worlds_base_path(self) -> Path:
        return self._test_base_path

    def get_uwp_store_path(self) -> Path:
        return self._test_base_path / "uwp_store"

    def get_shared_path(self, worlds_base_path: Path) -> Path:
        return self._test_base_path / "shared"

    # Herdar métodos do pai - FileSystemWorldRepository já implementa:
    # path_exists, list_directory, is_directory, read_text_file, calculate_total_size
    # que usam pathlib.Path métodos nativos


@pytest.fixture
def temp_dir() -> Generator[Path]:
    """Cria um diretório temporário que é limpo após o teste."""
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


@pytest.fixture
def test_worlds_base_path(temp_dir: Path) -> Path:
    """Cria diretório base para mundos de teste."""
    base = temp_dir / "minecraft_worlds"
    base.mkdir(parents=True, exist_ok=True)
    return base


@pytest.fixture
def fs_world_repo(test_worlds_base_path: Path):
    """Retorna repositório de mundos configurado para testes."""
    return TestFileSystemWorldRepository(test_worlds_base_path)


@pytest.fixture
def fs_backup_repo() -> FileSystemBackupRepository:
    """Retorna repositório de backup com filesystem real."""
    return FileSystemBackupRepository()


@pytest.fixture
def sample_world_dir(test_worlds_base_path: Path) -> Path:
    """Cria um diretório de mundo válido para testes no base path correto.

    Cria a estrutura esperada pelo WorldService:
    test_worlds_base_path / account_id / games / com.mojang / minecraftWorlds / world_folder
    """
    # Criar a estrutura de diretórios esperada pelo WorldService
    account_id = "test_account_123"
    world_dir = (
        test_worlds_base_path
        / account_id
        / "games"
        / "com.mojang"
        / "minecraftWorlds"
        / "6LknJ3qXcJo="
    )
    world_dir.mkdir(parents=True, exist_ok=True)

    # Criar levelname.txt
    (world_dir / "levelname.txt").write_text("Test World", encoding="utf-8")

    # Criar level.dat (arquivo dummy)
    (world_dir / "level.dat").write_bytes(b"dummy level data")

    # Criar alguns arquivos e subdiretórios para simular mundo real
    (world_dir / "db").mkdir()
    (world_dir / "db" / "leveldb").write_bytes(b"dummy db data")

    (world_dir / "region").mkdir()
    (world_dir / "region" / "r.0.0.mca").write_bytes(b"dummy region data")

    return world_dir


@pytest.fixture
def sample_world_model(sample_world_dir: Path) -> WorldModel:
    """Cria um WorldModel válido apontando para o diretório de teste."""
    from backup_manager_mvp.core.models.world_model import WorldModel

    return WorldModel(
        folder_name=sample_world_dir.name,
        levelname="Test World",
        world_icon_path=sample_world_dir / "world_icon.jpeg",
        path=sample_world_dir,
        account_id="test_account_123",
        version=[1, 26, 12, 2, 0],
    )


@pytest.fixture
def backup_base_dir(temp_dir: Path) -> Path:
    """Cria diretório base para backups."""
    backup_dir = temp_dir / "backups"
    backup_dir.mkdir()
    return backup_dir


@pytest.fixture
def fs_backup_repo_with_base(backup_base_dir: Path) -> FileSystemBackupRepository:
    """Retorna repositório de backup configurado com base dir customizado."""
    import backup_manager_mvp.utils.paths as paths_module

    # Monkey patch temporário do BACKUPS_DIR
    original_backups_dir = paths_module.BACKUPS_DIR
    paths_module.BACKUPS_DIR = backup_base_dir

    repo = FileSystemBackupRepository()

    # Restaurar após uso
    yield repo

    paths_module.BACKUPS_DIR = original_backups_dir
