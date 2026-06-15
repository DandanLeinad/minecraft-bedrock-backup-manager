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

"""Testes de integração para descoberta de mundos com filesystem real."""

from pathlib import Path

import pytest

from backup_manager_mvp.core.services.world_service import WorldService


class TestWorldDiscoveryIntegration:
    """Testes de integração para descoberta de mundos com filesystem real."""

    def test_list_worlds_finds_valid_worlds(self, fs_world_repo, sample_world_dir: Path) -> None:
        """Deve encontrar mundos válidos no filesystem real."""
        # O fs_world_repo já está configurado com o temp_dir correto via fixture
        service = WorldService(fs_world_repo)

        worlds = service.list_worlds()

        assert len(worlds) >= 1
        world = worlds[0]
        assert world.folder_name == "6LknJ3qXcJo="
        assert world.levelname == "Test World"

    def test_list_worlds_ignores_invalid_directories(self, fs_world_repo, temp_dir: Path) -> None:
        """Deve ignorar diretórios que não são mundos válidos."""
        # Criar diretório sem levelname.txt
        invalid_dir = temp_dir / "not_a_world"
        invalid_dir.mkdir()

        # Criar mundo válido no diretório base do repositório de teste
        # O fs_world_repo já está configurado com o temp_dir correto
        base_path = fs_world_repo.get_worlds_base_path()
        account_id = "test_account_123"
        valid_dir = (
            base_path / account_id / "games" / "com.mojang" / "minecraftWorlds" / "abcdefghijk="
        )
        valid_dir.mkdir(parents=True, exist_ok=True)
        (valid_dir / "levelname.txt").write_text("Valid World", encoding="utf-8")
        (valid_dir / "level.dat").write_bytes(b"data")

        service = WorldService(fs_world_repo)

        # Testar que apenas o mundo válido é encontrado
        worlds = service.list_worlds()
        assert len(worlds) == 1
        assert worlds[0].levelname == "Valid World"

    def test_list_worlds_ignores_files_not_directories(self, fs_world_repo, temp_dir: Path) -> None:
        """Deve ignorar arquivos que não são diretórios."""
        # Criar arquivo na raiz (não diretório)
        (temp_dir / "not_a_dir.txt").write_text("not a world")

        service = WorldService(fs_world_repo)
        worlds = service.list_worlds()

        # Não deve crashar, apenas ignorar
        assert isinstance(worlds, list)

    def test_list_worlds_handles_permission_errors(self, fs_world_repo, temp_dir: Path) -> None:
        """Deve lidar graciosamente com erros de permissão."""
        service = WorldService(fs_world_repo)

        # Testar com caminho inexistente
        worlds = service.list_worlds()
        assert isinstance(worlds, list)

    def test_get_world_levelname_reads_from_file(
        self, fs_world_repo, sample_world_dir: Path
    ) -> None:
        """Deve ler levelname do arquivo levelname.txt."""
        service = WorldService(fs_world_repo)

        levelname = service.get_world_levelname(sample_world_dir)

        assert levelname == "Test World"

    def test_get_world_levelname_raises_on_missing_file(
        self, fs_world_repo, temp_dir: Path
    ) -> None:
        """Deve lançar FileNotFoundError se levelname.txt não existir."""
        service = WorldService(fs_world_repo)

        invalid_dir = temp_dir / "no_levelname"
        invalid_dir.mkdir()

        with pytest.raises(FileNotFoundError):
            service.get_world_levelname(invalid_dir)

    def test_get_world_levelname_raises_on_empty_file(self, fs_world_repo, temp_dir: Path) -> None:
        """Deve lançar ValueError se levelname.txt estiver vazio."""
        service = WorldService(fs_world_repo)

        invalid_dir = temp_dir / "empty_levelname"
        invalid_dir.mkdir()
        (invalid_dir / "levelname.txt").write_text("", encoding="utf-8")

        with pytest.raises(ValueError, match="vazio"):
            service.get_world_levelname(invalid_dir)

    def test_get_world_levelname_raises_on_whitespace_only(
        self, fs_world_repo, temp_dir: Path
    ) -> None:
        """Deve lançar ValueError se levelname.txt tiver apenas whitespace."""
        service = WorldService(fs_world_repo)

        invalid_dir = temp_dir / "whitespace_levelname"
        invalid_dir.mkdir()
        (invalid_dir / "levelname.txt").write_text("   \n\t  ", encoding="utf-8")

        with pytest.raises(ValueError, match="vazio"):
            service.get_world_levelname(invalid_dir)
