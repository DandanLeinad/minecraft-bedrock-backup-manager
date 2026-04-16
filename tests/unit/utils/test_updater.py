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

"""Tests for update checker."""

import json
import tempfile
from pathlib import Path

from backup_manager_mvp.utils.updater import UpdateChecker, VersionInfo


class TestVersionInfo:
    """Test version parsing and comparison."""

    def test_parse_stable_version(self):
        """Test parsing stable version."""
        v = VersionInfo("v1.2.3")
        assert v.major == 1
        assert v.minor == 2
        assert v.patch == 3
        assert v.prerelease is None

    def test_parse_beta_version(self):
        """Test parsing beta version."""
        v = VersionInfo("v0.1.0-beta")
        assert v.major == 0
        assert v.minor == 1
        assert v.patch == 0
        assert v.prerelease == "beta"

    def test_parse_rc_version(self):
        """Test parsing release candidate version."""
        v = VersionInfo("1.0.0-rc.1")
        assert v.major == 1
        assert v.minor == 0
        assert v.patch == 0
        assert v.prerelease == "rc.1"

    def test_version_string_representation(self):
        """Test version string conversion."""
        v = VersionInfo("v1.2.3-beta")
        assert str(v) == "v1.2.3-beta"

    def test_version_comparison_major(self):
        """Test version comparison for major versions."""
        v1 = VersionInfo("v1.0.0")
        v2 = VersionInfo("v2.0.0")
        assert v1 < v2
        assert v2 > v1
        assert not (v1 >= v2)

    def test_version_comparison_minor(self):
        """Test version comparison for minor versions."""
        v1 = VersionInfo("v1.1.0")
        v2 = VersionInfo("v1.2.0")
        assert v1 < v2
        assert v2 > v1

    def test_version_comparison_patch(self):
        """Test version comparison for patch versions."""
        v1 = VersionInfo("v1.2.3")
        v2 = VersionInfo("v1.2.4")
        assert v1 < v2
        assert v2 > v1

    def test_version_comparison_prerelease(self):
        """Test that prerelease versions are less than stable."""
        v1 = VersionInfo("v1.0.0-beta")
        v2 = VersionInfo("v1.0.0")
        assert v1 < v2
        assert v2 > v1

    def test_version_equality(self):
        """Test version equality."""
        v1 = VersionInfo("v1.0.0")
        v2 = VersionInfo("v1.0.0")
        assert v1 == v2
        assert v1 <= v2
        assert v1 >= v2

    def test_version_inequality(self):
        """Test version inequality."""
        v1 = VersionInfo("v1.0.0")
        v2 = VersionInfo("v2.0.0")
        assert v1 != v2


class TestUpdateChecker:
    """Test update checker functionality."""

    def test_load_valid_version_json(self):
        """Test loading valid version.json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            version_file = Path(tmpdir) / "version.json"
            version_data = {
                "current": "v0.1.0-beta",
                "release_date": "2026-04-15",
                "check_for_updates": True,
            }
            with open(version_file, "w") as f:
                json.dump(version_data, f)

            checker = UpdateChecker(version_file)
            assert checker.load_local_version()
            assert checker.local_version is not None
            assert str(checker.local_version) == "v0.1.0-beta"

    def test_load_missing_version_json(self):
        """Test handling of missing version.json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            version_file = Path(tmpdir) / "nonexistent.json"
            checker = UpdateChecker(version_file)
            assert not checker.load_local_version()

    def test_load_invalid_json(self):
        """Test handling of invalid JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            version_file = Path(tmpdir) / "version.json"
            with open(version_file, "w") as f:
                f.write("invalid json")

            checker = UpdateChecker(version_file)
            assert not checker.load_local_version()

    def test_get_current_version(self):
        """Test getting current version."""
        with tempfile.TemporaryDirectory() as tmpdir:
            version_file = Path(tmpdir) / "version.json"
            version_data = {"current": "v1.2.3"}
            with open(version_file, "w") as f:
                json.dump(version_data, f)

            checker = UpdateChecker(version_file)
            assert checker.get_current_version() == "v1.2.3"

    def test_get_version_info(self):
        """Test getting version info."""
        with tempfile.TemporaryDirectory() as tmpdir:
            version_file = Path(tmpdir) / "version.json"
            version_data = {
                "current": "v0.1.0-beta",
                "release_date": "2026-04-15",
                "update_url": "https://github.com/...",
                "changelog_url": "https://github.com/...",
            }
            with open(version_file, "w") as f:
                json.dump(version_data, f)

            checker = UpdateChecker(version_file)
            info = checker.get_version_info()
            assert info["current"] == "v0.1.0-beta"
            assert info["release_date"] == "2026-04-15"

    def test_check_for_updates_disabled(self):
        """Test that updates are not checked when disabled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            version_file = Path(tmpdir) / "version.json"
            version_data = {
                "current": "v0.1.0-beta",
                "check_for_updates": False,
            }
            with open(version_file, "w") as f:
                json.dump(version_data, f)

            checker = UpdateChecker(version_file)
            assert not checker.check_for_updates()

    def test_check_for_updates_enabled(self):
        """Test update checking when enabled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            version_file = Path(tmpdir) / "version.json"
            version_data = {
                "current": "v0.1.0-beta",
                "check_for_updates": True,
            }
            with open(version_file, "w") as f:
                json.dump(version_data, f)

            checker = UpdateChecker(version_file)
            # Currently returns False (placeholder implementation)
            assert not checker.check_for_updates()

    def test_get_update_info(self):
        """Test getting update information."""
        with tempfile.TemporaryDirectory() as tmpdir:
            version_file = Path(tmpdir) / "version.json"
            version_data = {
                "current": "v0.1.0-beta",
                "update_url": "https://github.com/owner/repo/releases",
                "changelog_url": "https://github.com/owner/repo/CHANGELOG.md",
                "download_url": "https://github.com/owner/repo/releases/download/v0.1.0/app.exe",
                "release_date": "2026-04-15",
            }
            with open(version_file, "w") as f:
                json.dump(version_data, f)

            checker = UpdateChecker(version_file)
            update_info = checker.get_update_info()
            assert update_info["current"] == "v0.1.0-beta"
            assert update_info["update_url"] == "https://github.com/owner/repo/releases"
            assert (
                update_info["changelog_url"]
                == "https://github.com/owner/repo/CHANGELOG.md"
            )


class TestVersionComparisons:
    """Test various version comparison scenarios."""

    def test_beta_to_stable_progression(self):
        """Test progression from beta to stable."""
        versions = [
            VersionInfo("v0.1.0-beta"),
            VersionInfo("v0.1.0-rc.1"),
            VersionInfo("v0.1.0"),
        ]
        for i, v in enumerate(versions[:-1]):
            assert v < versions[i + 1]

    def test_complex_prerelease_names(self):
        """Test complex prerelease names."""
        v1 = VersionInfo("v1.0.0-alpha.1")
        v2 = VersionInfo("v1.0.0-beta.1")
        assert v1 < v2  # alpha < beta (string comparison)

    def test_missing_patch_version(self):
        """Test handling of missing patch version."""
        v = VersionInfo("v1.2")
        assert v.major == 1
        assert v.minor == 2
        assert v.patch == 0
