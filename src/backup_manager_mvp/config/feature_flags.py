# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

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
    ENABLE_WORLD_ICON_PREVIEW: bool = _parse_bool(os.getenv("FF_WORLD_ICON_PREVIEW", "true"))
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
