"""Global pytest configuration and fixtures."""

import pytest

# Domain markers - allow filtering: pytest -m "world and unit"
pytestmark = [
    pytest.mark.unit,
]


# Custom markers for domain filtering
def pytest_configure(config):
    config.addinivalue_line("markers", "world: marks tests for world domain")
    config.addinivalue_line("markers", "backup: marks tests for backup domain")
    config.addinivalue_line("markers", "progress: marks tests for progress domain")
    config.addinivalue_line("markers", "ui: marks tests for UI domain")
    config.addinivalue_line("markers", "utils: marks tests for utils domain")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "slow: marks tests as slow")


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
