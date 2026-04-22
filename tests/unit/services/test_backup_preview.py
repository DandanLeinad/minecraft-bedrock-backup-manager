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

"""Testes para BackupService.get_backup_preview_info() - MC-3 Restore Preview Feature."""

from datetime import datetime

import pytest

from backup_manager_mvp.models.backup_model import BackupModel
from backup_manager_mvp.services.backup_service import BackupService


class TestGetBackupPreviewInfo:
    """Testes para o método get_backup_preview_info()."""

    @pytest.fixture
    def backup_service(self):
        """Fixture para BackupService."""
        return BackupService()

    @pytest.fixture
    def sample_backup_with_content(self, tmp_path):
        """Fixture: Backup com conteúdo (arquivos e diretórios)."""
        backup_path = tmp_path / "backups" / "test_world" / "2026-04-22_12-00-00"
        backup_path.mkdir(parents=True, exist_ok=True)

        # Criar estrutura de exemplo
        (backup_path / "level.dat").write_text("mock level data")  # 15 bytes
        (backup_path / "level.dat_old").write_text("old backup")  # 10 bytes

        world_dir = backup_path / "world"
        world_dir.mkdir()
        (world_dir / "chunk_file1.mcr").write_text("chunk data 1")  # 12 bytes
        (world_dir / "chunk_file2.mcr").write_text("chunk data 22")  # 13 bytes

        db_dir = backup_path / "db"
        db_dir.mkdir()
        (db_dir / "000000.ldb").write_text("database file")  # 13 bytes

        backup = BackupModel(
            world_folder_name="test_world",
            world_account_id="account123",
            created_at=datetime(2026, 4, 22, 12, 0, 0),
            backup_path=backup_path,
        )

        return backup

    def test_get_backup_preview_info_returns_dict(self, backup_service, sample_backup_with_content):
        """Testa que get_backup_preview_info retorna um dicionário."""
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        assert isinstance(result, dict)
        assert "total_files" in result
        assert "total_dirs" in result
        assert "total_size" in result
        assert "top_level_items" in result
        assert "error" in result

    def test_get_backup_preview_info_counts_files_correctly(
        self, backup_service, sample_backup_with_content
    ):
        """Testa que o método conta arquivos corretamente."""
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        # 2 arquivos no nível raiz + 2 em world + 1 em db = 5 total
        assert result["total_files"] == 5
        assert result["error"] is None

    def test_get_backup_preview_info_counts_dirs_correctly(
        self, backup_service, sample_backup_with_content
    ):
        """Testa que o método conta diretórios corretamente."""
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        # 2 diretórios no nível 1: world, db
        assert result["total_dirs"] == 2
        assert result["error"] is None

    def test_get_backup_preview_info_calculates_size(
        self, backup_service, sample_backup_with_content
    ):
        """Testa que o método calcula tamanho total corretamente."""
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        # 15 + 10 + (12 + 13) + 13 = 63 bytes
        assert result["total_size"] == 63
        assert result["error"] is None

    def test_get_backup_preview_info_lists_top_level_items(
        self, backup_service, sample_backup_with_content
    ):
        """Testa que o método lista itens do nível 1."""
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        items = result["top_level_items"]
        assert len(items) == 4  # 2 arquivos + 2 diretórios

        # Verificar formato
        for item in items:
            assert "name" in item
            assert "type" in item
            assert "size" in item
            assert item["type"] in ("file", "dir")

    def test_get_backup_preview_info_sorts_dirs_first(
        self, backup_service, sample_backup_with_content
    ):
        """Testa que diretórios aparecem antes de arquivos."""
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        items = result["top_level_items"]
        # Primeiros itens devem ser diretórios
        for item in items:
            if item["type"] == "dir":
                # Após encontrar um dir, não deve haver files antes
                assert True
            elif item["type"] == "file":
                # Uma vez em files, verificar que não há mais dirs
                remaining = items[items.index(item) + 1 :]
                for remaining_item in remaining:
                    assert remaining_item["type"] != "dir"
                break

    def test_get_backup_preview_info_nonexistent_backup(self, backup_service, tmp_path):
        """Testa que retorna erro para backup inexistente."""
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

    def test_get_backup_preview_info_empty_backup(self, backup_service, tmp_path):
        """Testa backup vazio (apenas a pasta, sem conteúdo)."""
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

    def test_get_backup_preview_info_large_file_list_truncated(self, backup_service, tmp_path):
        """Testa que lista grande de itens é truncada a 20."""
        backup_path = tmp_path / "many_files_backup"
        backup_path.mkdir(parents=True, exist_ok=True)

        # Criar 25 arquivos
        for i in range(25):
            (backup_path / f"file_{i}.dat").write_text(f"content {i}")

        backup = BackupModel(
            world_folder_name="many_files",
            world_account_id="account123",
            created_at=datetime(2026, 4, 22, 12, 0, 0),
            backup_path=backup_path,
        )

        result = backup_service.get_backup_preview_info(backup)

        # Deve ter 20 + 1 ellipsis item
        assert len(result["top_level_items"]) == 21
        assert result["top_level_items"][-1]["type"] == "ellipsis"
        assert result["top_level_items"][-1]["name"] == "... e mais itens"

    def test_get_backup_preview_info_size_calculated_for_dirs(
        self, backup_service, sample_backup_with_content
    ):
        """Testa que tamanho de diretórios inclui arquivos recursivos."""
        result = backup_service.get_backup_preview_info(sample_backup_with_content)

        items = result["top_level_items"]
        world_item = next((i for i in items if i["name"] == "world"), None)

        assert world_item is not None
        # world tem 2 arquivos: 12 + 13 = 25 bytes
        assert world_item["size"] == 25
