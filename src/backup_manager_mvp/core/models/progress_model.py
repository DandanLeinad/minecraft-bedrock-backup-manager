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

"""Model for tracking operation progress (backup/restore)."""

from dataclasses import dataclass


@dataclass
class ProgressModel:
    """Model for tracking progress of an operation.

    Generic and reusable for any service (backup, restore, cloud sync, etc).

    Attributes:
        current: Number of items processed
        total: Total number of items
        stage: Description of current stage (e.g., "Copying files...")

    Raises:
        ValueError: If current < 0 or total <= 0
    """

    current: int
    total: int
    stage: str = ""

    def __post_init__(self) -> None:
        """Validation after initialization."""
        if self.current < 0:
            raise ValueError("current must be non-negative")
        if self.total <= 0:
            raise ValueError("total must be greater than 0")

    @property
    def percentage(self) -> float:
        """Calculate the progress percentage (0-100).

        Returns:
            float: Completion percentage (0.0 to 100.0), capped at 100%

        Example:
            >>> progress = ProgressModel(current=5, total=10, stage="Processing")
            >>> progress.percentage
            50.0
        """
        percentage = (self.current / self.total) * 100.0
        # Cap at 100% maximum
        return min(percentage, 100.0)

    def is_complete(self) -> bool:
        """Check if the operation is complete.

        Returns:
            bool: True if current == total

        Example:
            >>> progress = ProgressModel(current=10, total=10, stage="Done")
            >>> progress.is_complete()
            True
        """
        return self.current == self.total
