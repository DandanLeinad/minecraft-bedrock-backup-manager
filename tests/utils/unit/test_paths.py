# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

"""Tests for centralized path configuration."""

from pathlib import Path

from backup_manager_mvp.utils.paths import (
    BACKUPS_DIR,
    BACKUPS_ROOT,
    LOG_FILE,
    ensure_directories,
)


class TestPathsConstants:
    """Tests for path constants.

    Rules:
    - BACKUPS_ROOT is a Path object containing 'Documents' and 'MinecraftBackups'
    - LOG_FILE is a Path object inside BACKUPS_ROOT named 'app.log'
    - BACKUPS_DIR is a Path object inside BACKUPS_ROOT named 'backups'
    """

    def test_should_be_path_object_for_backups_root(self):
        """
        BACKUPS_ROOT should be a Path object.
        """
        assert isinstance(BACKUPS_ROOT, Path)

    def test_should_contain_documents_in_path(self):
        """
        BACKUPS_ROOT should contain 'Documents' in its path.
        """
        assert "Documents" in str(BACKUPS_ROOT)

    def test_should_contain_minecraft_backups_in_path(self):
        """
        BACKUPS_ROOT should contain 'MinecraftBackups' in its path.
        """
        assert "MinecraftBackups" in str(BACKUPS_ROOT)

    def test_should_be_path_object_for_log_file(self):
        """
        LOG_FILE should be a Path object.
        """
        assert isinstance(LOG_FILE, Path)

    def test_should_be_inside_backups_root_for_log_file(self):
        """
        LOG_FILE should be located inside BACKUPS_ROOT.
        """
        assert LOG_FILE.parent == BACKUPS_ROOT

    def test_should_be_named_app_log(self):
        """
        LOG_FILE should be named 'app.log'.
        """
        assert LOG_FILE.name == "app.log"

    def test_should_be_path_object_for_backups_dir(self):
        """
        BACKUPS_DIR should be a Path object.
        """
        assert isinstance(BACKUPS_DIR, Path)

    def test_should_be_inside_backups_root_for_backups_dir(self):
        """
        BACKUPS_DIR should be located inside BACKUPS_ROOT.
        """
        assert BACKUPS_DIR.parent == BACKUPS_ROOT

    def test_should_be_named_backups(self):
        """
        BACKUPS_DIR should be named 'backups'.
        """
        assert BACKUPS_DIR.name == "backups"


class TestEnsureDirectories:
    """Tests for ensure_directories function.

    Rules:
    - Creates BACKUPS_ROOT if it doesn't exist
    - Creates BACKUPS_DIR if it doesn't exist
    - Is idempotent (safe to call multiple times)
    - Creates nested directory structure
    """

    def test_should_create_backups_root(self, tmp_path, monkeypatch):
        """
        ensure_directories should create BACKUPS_ROOT directory.
        """
        # Mock BACKUPS_ROOT to tmp_path
        test_backups_root = tmp_path / "TestBackups"
        monkeypatch.setattr("backup_manager_mvp.utils.paths.BACKUPS_ROOT", test_backups_root)

        # Should not exist yet
        assert not test_backups_root.exists()

        # Call ensure_directories
        ensure_directories()

        # Now should exist
        assert test_backups_root.exists()
        assert test_backups_root.is_dir()

    def test_should_create_backups_dir(self, tmp_path, monkeypatch):
        """
        ensure_directories should create BACKUPS_DIR directory.
        """
        # Mock the paths
        test_backups_root = tmp_path / "TestBackups"
        test_backups_dir = test_backups_root / "backups"

        monkeypatch.setattr("backup_manager_mvp.utils.paths.BACKUPS_ROOT", test_backups_root)
        monkeypatch.setattr("backup_manager_mvp.utils.paths.BACKUPS_DIR", test_backups_dir)

        # Should not exist yet
        assert not test_backups_dir.exists()

        # Call ensure_directories
        ensure_directories()

        # Now should exist
        assert test_backups_dir.exists()
        assert test_backups_dir.is_dir()

    def test_should_be_idempotent(self, tmp_path, monkeypatch):
        """
        ensure_directories should be idempotent (safe to call multiple times).
        """
        test_backups_root = tmp_path / "TestBackups"
        test_backups_dir = test_backups_root / "backups"

        monkeypatch.setattr("backup_manager_mvp.utils.paths.BACKUPS_ROOT", test_backups_root)
        monkeypatch.setattr("backup_manager_mvp.utils.paths.BACKUPS_DIR", test_backups_dir)

        # First call
        ensure_directories()
        assert test_backups_root.exists()
        assert test_backups_dir.exists()

        # Second call (should not raise error)
        ensure_directories()
        assert test_backups_root.exists()
        assert test_backups_dir.exists()

    def test_should_create_nested_structure(self, tmp_path, monkeypatch):
        """
        ensure_directories should create complete nested directory structure.
        """
        # Mock with deeply nested path
        test_backups_root = tmp_path / "deep" / "nested" / "path" / "TestBackups"
        test_backups_dir = test_backups_root / "backups"

        monkeypatch.setattr("backup_manager_mvp.utils.paths.BACKUPS_ROOT", test_backups_root)
        monkeypatch.setattr("backup_manager_mvp.utils.paths.BACKUPS_DIR", test_backups_dir)

        # Call ensure_directories
        ensure_directories()

        # Both should exist
        assert test_backups_root.exists()
        assert test_backups_dir.exists()
