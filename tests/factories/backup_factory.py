# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad

"""Factory for creating BackupModel instances in tests."""

from datetime import datetime
from pathlib import Path

from backup_manager_mvp.core.models.backup_model import BackupModel


class BackupFactory:
    """Factory for creating valid BackupModel instances with minimal boilerplate."""

    _DEFAULT_WORLD_FOLDER_NAME = "6LknJ3qXcJo="
    _DEFAULT_WORLD_ACCOUNT_ID = "123456789012345678"

    @staticmethod
    def create(**overrides) -> BackupModel:
        """
        Create a valid BackupModel with sensible defaults.

        Args:
            **overrides: Any field to override (world_folder_name, world_account_id, created_at, backup_path)

        Returns:
            A valid BackupModel instance.
        """
        backup_path = overrides.get("backup_path", Path("/fake/backups/2024-01-15_10-30-00"))

        data = {
            "world_folder_name": overrides.get(
                "world_folder_name", BackupFactory._DEFAULT_WORLD_FOLDER_NAME
            ),
            "world_account_id": overrides.get(
                "world_account_id", BackupFactory._DEFAULT_WORLD_ACCOUNT_ID
            ),
            "created_at": overrides.get("created_at", datetime(2024, 1, 15, 10, 30, 0)),
            "backup_path": backup_path,
        }

        # Apply any remaining overrides
        data.update({k: v for k, v in overrides.items() if k not in data})

        return BackupModel(**data)
