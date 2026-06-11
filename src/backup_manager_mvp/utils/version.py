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

"""Version information and utilities for Minecraft Bedrock Backup Manager."""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

__version__ = "v0.1.0-beta"


def get_app_version() -> str:
    """Get application version from version.json.

    Returns:
        Application version string
    """
    try:
        version_file = Path(__file__).parent.parent / "version.json"
        if version_file.exists():
            with open(version_file, encoding="utf-8") as f:
                data = json.load(f)
                return data.get("current", __version__)
    except (json.JSONDecodeError, OSError) as e:
        logger.debug(f"Could not read version.json: {e}")

    return __version__


class VersionInfo:
    """Parse and compare semantic version strings.

    Supports formats: MAJOR.MINOR.PATCH[-PRERELEASE]
    Examples: "1.0.0", "1.2.3-beta", "0.5.0b0", "v1.0.0-rc.1"
    """

    def __init__(self, version_str: str):
        """Parse version string.

        Args:
            version_str: Version string in format MAJOR.MINOR.PATCH[-PRERELEASE]
        """
        self.original = version_str
        self._parse(version_str)

    def _parse(self, version_str: str) -> None:
        """Parse version string into components.

        Args:
            version_str: Version string to parse
        """
        # Remove 'v' prefix if present
        if version_str.startswith("v"):
            version_str = version_str[1:]

        # Split prerelease
        if "-" in version_str:
            base, prerelease = version_str.split("-", 1)
            self.prerelease = prerelease
        else:
            base = version_str
            self.prerelease = None

        # Split major.minor.patch
        parts = base.split(".")
        try:
            self.major = int(parts[0]) if len(parts) > 0 else 0
            self.minor = int(parts[1]) if len(parts) > 1 else 0
            self.patch = int(parts[2]) if len(parts) > 2 else 0
        except ValueError, IndexError:
            logger.warning(f"Could not parse version: {version_str}")
            self.major = 0
            self.minor = 0
            self.patch = 0

    def __lt__(self, other: VersionInfo) -> bool:
        """Check if this version is less than other."""
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        if self.patch != other.patch:
            return self.patch < other.patch

        # Both non-prerelease or both prerelease
        if self.prerelease is None and other.prerelease is None:
            return False  # Equal
        if self.prerelease is None:
            return False  # Non-prerelease > prerelease
        if other.prerelease is None:
            return True  # Prerelease < non-prerelease

        # Both prerelease, simple string comparison
        return self.prerelease < other.prerelease

    def __le__(self, other: VersionInfo) -> bool:
        """Check if this version is <= other."""
        return self < other or str(self) == str(other)

    def __gt__(self, other: VersionInfo) -> bool:
        """Check if this version is greater than other."""
        return not self <= other

    def __ge__(self, other: VersionInfo) -> bool:
        """Check if this version is >= other."""
        return not self < other

    def __eq__(self, other: object) -> bool:
        """Check if versions are equal."""
        if not isinstance(other, VersionInfo):
            return False
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
            and self.prerelease == other.prerelease
        )

    def __str__(self) -> str:
        """String representation with 'v' prefix."""
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version += f"-{self.prerelease}"
        return f"v{version}"


# Initialize version at module load
__version__ = get_app_version()
