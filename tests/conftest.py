# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad

"""Global pytest configuration and fixtures."""

from pathlib import Path

import pytest


# Custom markers for domain filtering
def pytest_configure(config):
    config.addinivalue_line("markers", "world: marks tests for world domain")
    config.addinivalue_line("markers", "backup: marks tests for backup domain")
    config.addinivalue_line("markers", "progress: marks tests for progress domain")
    config.addinivalue_line("markers", "ui: marks tests for UI domain")
    config.addinivalue_line("markers", "utils: marks tests for utils domain")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "slow: marks tests as slow")


def pytest_collection_modifyitems(config, items):
    """Auto-apply markers based on test file path."""
    tests_root = Path(str(config.rootpath)) / "tests"
    for item in items:
        # Get the relative path from tests/
        item_path = Path(str(item.fspath))
        try:
            rel_path = str(item_path.relative_to(tests_root))
        except ValueError:
            continue

        # Normalize path separators for cross-platform matching
        norm_path = rel_path.replace("\\", "/")

        # Apply domain markers based on path
        if norm_path.startswith("world/"):
            item.add_marker(pytest.mark.world)
        elif norm_path.startswith("backup/"):
            item.add_marker(pytest.mark.backup)
        elif norm_path.startswith("progress/"):
            item.add_marker(pytest.mark.progress)
        elif norm_path.startswith("ui/"):
            item.add_marker(pytest.mark.ui)
        elif norm_path.startswith("utils/"):
            item.add_marker(pytest.mark.utils)

        # Apply type markers based on path
        if "/integration/" in norm_path:
            item.add_marker(pytest.mark.integration)
        elif "/unit/" in norm_path:
            item.add_marker(pytest.mark.unit)


@pytest.fixture
def world_factory():
    """Provide WorldFactory for tests."""
    from tests.factories.world_factory import WorldFactory

    return WorldFactory


@pytest.fixture
def backup_factory():
    """Provide BackupFactory for tests."""
    from tests.factories.backup_factory import BackupFactory

    return BackupFactory
