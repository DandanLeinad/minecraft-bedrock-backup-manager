# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad

"""Factory for creating WorldModel instances in tests."""

from pathlib import Path
from typing import ClassVar

from backup_manager_mvp.core.models.world_model import WorldModel


class WorldFactory:
    """Factory for creating valid WorldModel instances with minimal boilerplate."""

    _DEFAULT_FOLDER_NAME: ClassVar[str] = "6LknJ3qXcJo="
    _DEFAULT_LEVELNAME: ClassVar[str] = "Test World"
    _DEFAULT_ACCOUNT_ID: ClassVar[str] = "123456789012345678"
    _DEFAULT_VERSION: ClassVar[list[int]] = [1, 21, 0, 0, 0]

    @staticmethod
    def create(**overrides) -> WorldModel:
        """
        Create a valid WorldModel with sensible defaults.

        Args:
            **overrides: Any field to override (folder_name, levelname, path, etc.)

        Returns:
            A valid WorldModel instance.
        """
        # Build path from folder_name if not provided
        folder_name = overrides.get("folder_name", WorldFactory._DEFAULT_FOLDER_NAME)
        path = overrides.get("path", Path(f"/fake/worlds/{folder_name}"))
        world_icon_path = overrides.get("world_icon_path", path / "world_icon.jpeg")

        data = {
            "folder_name": folder_name,
            "levelname": overrides.get("levelname", WorldFactory._DEFAULT_LEVELNAME),
            "world_icon_path": world_icon_path,
            "path": path,
            "account_id": overrides.get("account_id", WorldFactory._DEFAULT_ACCOUNT_ID),
            "version": overrides.get("version", WorldFactory._DEFAULT_VERSION),
        }

        # Apply any remaining overrides
        data.update({k: v for k, v in overrides.items() if k not in data})

        return WorldModel(**data)
