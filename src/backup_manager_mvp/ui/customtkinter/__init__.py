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
    "BackupCache",
    "COLORS",
    "BUTTON_HEIGHT",
    "APP_TITLE",
    "SPACING_SMALL",
    "SPACING_MEDIUM",
    "SPACING_LARGE",
    "WINDOW_MIN_HEIGHT",
    "WINDOW_MIN_WIDTH",
    "WINDOW_PREFERRED_HEIGHT",
    "WINDOW_PREFERRED_WIDTH",
    "configure_theme",
]
