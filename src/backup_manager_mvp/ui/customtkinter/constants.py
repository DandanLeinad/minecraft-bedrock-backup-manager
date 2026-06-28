# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

"""Constantes e configurações da UI CustomTkinter.

Contém:
- Paleta de cores profissional (tema Minecraft + Azul)
- Dimensões de janela e componentes
- Espaçamentos padrão
"""

from backup_manager_mvp.utils.version import __version__

# ========== PALHETA DE CORES CUSTOM PROFISSIONAL ==========
# Tema: Azul Minecraft com roxo complementar
# Formato: (light_mode, dark_mode) ou hex único

COLORS = {
    # Backgrounds
    "bg_primary_light": "#F5F7FA",
    "bg_primary_dark": "#1A1A2E",
    "bg_secondary_light": "#EEF2F5",
    "bg_secondary_dark": "#16213E",
    # Accents
    "accent_blue": "#0066FF",
    "accent_blue_hover": "#0052CC",
    "accent_green": "#00C853",
    "accent_green_hover": "#009C3B",
    "accent_red": "#FF3B30",
    "accent_red_hover": "#E02D22",
    "accent_orange": "#FF9500",
    # Text
    "text_primary": ("#1A1A1A", "#FFFFFF"),
    "text_secondary": ("#666666", "#CCCCCC"),
    "text_muted": ("#999999", "#999999"),
}

# ========== DIMENSÕES DE JANELA ==========

APP_TITLE = f"Minecraft Bedrock Backup Manager {__version__}"
WINDOW_MIN_WIDTH = 500
WINDOW_PREFERRED_WIDTH = 700
WINDOW_MIN_HEIGHT = 400
WINDOW_PREFERRED_HEIGHT = 600

# ========== ESPAÇAMENTOS ==========

SPACING_SMALL = 8
SPACING_MEDIUM = 16
SPACING_LARGE = 24

# ========== COMPONENTES ==========

BUTTON_HEIGHT = 44
