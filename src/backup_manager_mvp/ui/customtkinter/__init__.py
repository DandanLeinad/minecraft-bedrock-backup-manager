# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

"""Pacote CustomTkinter UI - Implementação da UI em CustomTkinter 5.2.2.

Estrutura:
- constants.py: Paleta de cores, dimensões, constantes
- theme.py: Configuração de tema
- cache.py: Cache de backups
- controller.py: Controlador principal (Phase 5)
- components/: Widgets reutilizáveis (Phase 2)
- screens/: Telas da aplicação (Phase 3)
- handlers/: Handlers de eventos (Phase 4)
- utils/: Funções auxiliares (Phase 2)
"""

from backup_manager_mvp.ui.customtkinter.cache import BackupCache
from backup_manager_mvp.ui.customtkinter.constants import (
    APP_TITLE,
    BUTTON_HEIGHT,
    COLORS,
    SPACING_LARGE,
    SPACING_MEDIUM,
    SPACING_SMALL,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_PREFERRED_HEIGHT,
    WINDOW_PREFERRED_WIDTH,
)
from backup_manager_mvp.ui.customtkinter.theme import configure_theme

__all__ = [
    "APP_TITLE",
    "BUTTON_HEIGHT",
    "COLORS",
    "SPACING_LARGE",
    "SPACING_MEDIUM",
    "SPACING_SMALL",
    "WINDOW_MIN_HEIGHT",
    "WINDOW_MIN_WIDTH",
    "WINDOW_PREFERRED_HEIGHT",
    "WINDOW_PREFERRED_WIDTH",
    "BackupCache",
    "configure_theme",
]
