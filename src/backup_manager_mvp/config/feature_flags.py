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

"""Feature flags para features em desenvolvimento.

Use para integrar código inacabado sem quebrar produção:

    ENABLE_AUTO_BACKUP = True      → Auto-backup em background
    ENABLE_CLOUD_SYNC = True       → Sincronização com cloud
    ENABLE_RESTORE_PREVIEW = True  → Preview antes de restaurar

Ativar via variável de ambiente:
    FF_AUTO_BACKUP=true uv run python -m backup_manager_mvp.main
"""

import logging
import os
from dataclasses import dataclass

logger = logging.getLogger(__name__)


def _parse_bool(value: str) -> bool:
    """Parse string para booleano."""
    return value.lower() in ("true", "1", "yes", "on")


@dataclass(frozen=True)
class FeatureFlags:
    """Feature flags da aplicação (imutável)."""

    # Features em desenvolvimento
    ENABLE_AUTO_BACKUP: bool = _parse_bool(os.getenv("FF_AUTO_BACKUP", "false"))
    ENABLE_CLOUD_SYNC: bool = _parse_bool(os.getenv("FF_CLOUD_SYNC", "false"))
    ENABLE_RESTORE_PREVIEW: bool = _parse_bool(os.getenv("FF_RESTORE_PREVIEW", "true"))

    # Features experimentais
    ENABLE_MULTI_THREADING: bool = _parse_bool(os.getenv("FF_MULTI_THREADING", "false"))
    ENABLE_ADVANCED_LOGGING: bool = _parse_bool(os.getenv("FF_ADVANCED_LOGGING", "false"))

    def __post_init__(self):
        """Log flags ativadas no init."""
        enabled_flags = [name for name in self.__dataclass_fields__ if getattr(self, name) is True]
        if enabled_flags:
            logger.info(f"Feature flags ativadas: {', '.join(enabled_flags)}")


# Instância global
FEATURE_FLAGS = FeatureFlags()
