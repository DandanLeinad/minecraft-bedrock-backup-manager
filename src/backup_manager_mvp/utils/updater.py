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

"""Auto-update checker for Minecraft Bedrock Backup Manager."""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class VersionInfo:
    """Holds version information."""

    def __init__(self, version_str: str):
        """Parse version string (e.g., '0.1.0-beta').

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
        """Check if this version is less than other.

        Args:
            other: Version to compare

        Returns:
            True if self < other
        """
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
        """Check if this version is <= other.

        Args:
            other: Version to compare

        Returns:
            True if self <= other
        """
        return self < other or str(self) == str(other)

    def __gt__(self, other: VersionInfo) -> bool:
        """Check if this version is greater than other.

        Args:
            other: Version to compare

        Returns:
            True if self > other
        """
        return not self <= other

    def __ge__(self, other: VersionInfo) -> bool:
        """Check if this version is >= other.

        Args:
            other: Version to compare

        Returns:
            True if self >= other
        """
        return not self < other

    def __eq__(self, other: object) -> bool:
        """Check if versions are equal.

        Args:
            other: Version to compare

        Returns:
            True if equal
        """
        if not isinstance(other, VersionInfo):
            return False
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
            and self.prerelease == other.prerelease
        )

    def __str__(self) -> str:
        """String representation.

        Returns:
            Version string with 'v' prefix
        """
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version += f"-{self.prerelease}"
        return f"v{version}"


class UpdateChecker:
    """Checks for application updates."""

    def __init__(self, version_file: Path | None = None):
        """Initialize update checker.

        Args:
            version_file: Path to version.json file
        """
        if version_file is None:
            # Try to find version.json in package
            version_file = Path(__file__).parent.parent / "version.json"

        self.version_file = version_file
        self.local_version: VersionInfo | None = None
        self.remote_version: VersionInfo | None = None
        self.update_available = False

    def load_local_version(self) -> bool:
        """Load local version from version.json.

        Returns:
            True if loaded successfully
        """
        try:
            if not self.version_file.exists():
                logger.warning(f"Version file not found: {self.version_file}")
                return False

            with open(self.version_file, encoding="utf-8") as f:
                data = json.load(f)

            current = data.get("current", "0.0.0")
            self.local_version = VersionInfo(current)
            logger.info(f"Local version: {self.local_version}")
            return True

        except (OSError, json.JSONDecodeError) as e:
            logger.error(f"Error loading version file: {e}")
            return False

    def get_version_info(self) -> dict:
        """Get current version information.

        Returns:
            Dictionary with version info
        """
        if self.local_version is None:
            self.load_local_version()

        try:
            with open(self.version_file, encoding="utf-8") as f:
                return json.load(f)
        except OSError, json.JSONDecodeError:
            return {
                "current": "v0.0.0",
                "release_date": "unknown",
                "check_for_updates": True,
            }

    def check_for_updates(self) -> bool:
        """Check if updates are available (placeholder for future API integration).

        Note: This is a simple check that returns False for now.
        In the future, this can be enhanced to:
        - Fetch from GitHub API
        - Check semver constraints
        - Validate checksums

        Returns:
            True if update available
        """
        try:
            if not self.load_local_version():
                return False

            version_info = self.get_version_info()

            # Check if updates are disabled
            if not version_info.get("check_for_updates", True):
                logger.info("Update checking is disabled")
                return False

            # For now, always return False (update check is placeholder)
            # In the future, implement actual remote version check
            logger.debug("Update check completed (no updates available)")
            self.update_available = False
            return False

        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
            return False

    def get_current_version(self) -> str:
        """Get current version string.

        Returns:
            Current version with 'v' prefix
        """
        if self.local_version is None:
            self.load_local_version()

        return str(self.local_version) if self.local_version else "v0.0.0"

    def get_update_info(self) -> dict:
        """Get update information from version.json.

        Returns:
            Dictionary with update URLs and info
        """
        version_info = self.get_version_info()
        return {
            "current": version_info.get("current", "0.0.0"),
            "update_url": version_info.get("update_url", ""),
            "changelog_url": version_info.get("changelog_url", ""),
            "download_url": version_info.get("download_url", ""),
            "release_date": version_info.get("release_date", "unknown"),
        }
