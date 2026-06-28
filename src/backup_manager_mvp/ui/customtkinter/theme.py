# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

"""Configuração de tema CustomTkinter.

Responsável por:
- Configurar modo de aparência (System, Dark, Light)
- Configurar tema de cores padrão
"""

import customtkinter as ctk


def configure_theme(appearance_mode: str = "System", color_theme: str = "blue") -> None:
    """Configura o tema da aplicação CustomTkinter.

    Args:
        appearance_mode: "System", "Dark" ou "Light"
        color_theme: "blue", "green", "dark-blue", etc.
    """
    ctk.set_appearance_mode(appearance_mode)
    ctk.set_default_color_theme(color_theme)
