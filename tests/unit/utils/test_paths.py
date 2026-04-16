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

"""Testes para a configuração de paths centralizada."""

from pathlib import Path

from backup_manager_mvp.utils.paths import (
    BACKUPS_DIR,
    BACKUPS_ROOT,
    LOG_FILE,
    ensure_directories,
)


class TestPathsConstants:
    """Testa constantes de paths."""

    def test_backups_root_is_path(self):
        """BACKUPS_ROOT deve ser um Path object."""
        assert isinstance(BACKUPS_ROOT, Path)

    def test_backups_root_contains_documents(self):
        """BACKUPS_ROOT deve conter 'Documents' no caminho."""
        assert "Documents" in str(BACKUPS_ROOT)

    def test_backups_root_contains_minecraft_backups(self):
        """BACKUPS_ROOT deve conter 'MinecraftBackups' no caminho."""
        assert "MinecraftBackups" in str(BACKUPS_ROOT)

    def test_log_file_is_path(self):
        """LOG_FILE deve ser um Path object."""
        assert isinstance(LOG_FILE, Path)

    def test_log_file_inside_backups_root(self):
        """LOG_FILE deve estar dentro de BACKUPS_ROOT."""
        assert LOG_FILE.parent == BACKUPS_ROOT

    def test_log_file_named_app_log(self):
        """LOG_FILE deve ser nomeado 'app.log'."""
        assert LOG_FILE.name == "app.log"

    def test_backups_dir_is_path(self):
        """BACKUPS_DIR deve ser um Path object."""
        assert isinstance(BACKUPS_DIR, Path)

    def test_backups_dir_inside_backups_root(self):
        """BACKUPS_DIR deve estar dentro de BACKUPS_ROOT."""
        assert BACKUPS_DIR.parent == BACKUPS_ROOT

    def test_backups_dir_named_backups(self):
        """BACKUPS_DIR deve ser nomeado 'backups'."""
        assert BACKUPS_DIR.name == "backups"


class TestEnsureDirectories:
    """Testa função ensure_directories."""

    def test_ensure_directories_creates_backups_root(self, tmp_path, monkeypatch):
        """ensure_directories deve criar BACKUPS_ROOT."""
        # Mock BACKUPS_ROOT para tmp_path
        test_backups_root = tmp_path / "TestBackups"
        monkeypatch.setattr(
            "backup_manager_mvp.utils.paths.BACKUPS_ROOT", test_backups_root
        )

        # Não deve existir ainda
        assert not test_backups_root.exists()

        # Chamar ensure_directories
        ensure_directories()

        # Agora deve existir
        assert test_backups_root.exists()
        assert test_backups_root.is_dir()

    def test_ensure_directories_creates_backups_dir(self, tmp_path, monkeypatch):
        """ensure_directories deve criar BACKUPS_DIR."""
        # Mock dos paths
        test_backups_root = tmp_path / "TestBackups"
        test_backups_dir = test_backups_root / "backups"

        monkeypatch.setattr(
            "backup_manager_mvp.utils.paths.BACKUPS_ROOT", test_backups_root
        )
        monkeypatch.setattr(
            "backup_manager_mvp.utils.paths.BACKUPS_DIR", test_backups_dir
        )

        # Não deve existir ainda
        assert not test_backups_dir.exists()

        # Chamar ensure_directories
        ensure_directories()

        # Agora deve existir
        assert test_backups_dir.exists()
        assert test_backups_dir.is_dir()

    def test_ensure_directories_idempotent(self, tmp_path, monkeypatch):
        """ensure_directories deve ser idempotente (chamar múltiplas vezes é seguro)."""
        test_backups_root = tmp_path / "TestBackups"
        test_backups_dir = test_backups_root / "backups"

        monkeypatch.setattr(
            "backup_manager_mvp.utils.paths.BACKUPS_ROOT", test_backups_root
        )
        monkeypatch.setattr(
            "backup_manager_mvp.utils.paths.BACKUPS_DIR", test_backups_dir
        )

        # Primeira chamada
        ensure_directories()
        assert test_backups_root.exists()
        assert test_backups_dir.exists()

        # Segunda chamada (não deve causar erro)
        ensure_directories()
        assert test_backups_root.exists()
        assert test_backups_dir.exists()

    def test_ensure_directories_creates_nested_structure(self, tmp_path, monkeypatch):
        """ensure_directories deve criar estrutura aninhada completa."""
        # Mock com path profundamente aninhado
        test_backups_root = tmp_path / "deep" / "nested" / "path" / "TestBackups"
        test_backups_dir = test_backups_root / "backups"

        monkeypatch.setattr(
            "backup_manager_mvp.utils.paths.BACKUPS_ROOT", test_backups_root
        )
        monkeypatch.setattr(
            "backup_manager_mvp.utils.paths.BACKUPS_DIR", test_backups_dir
        )

        # Chamar ensure_directories
        ensure_directories()

        # Ambas devem existir
        assert test_backups_root.exists()
        assert test_backups_dir.exists()
