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

"""Version information for Minecraft Bedrock Backup Manager."""

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


# Initialize version at module load
__version__ = get_app_version()
