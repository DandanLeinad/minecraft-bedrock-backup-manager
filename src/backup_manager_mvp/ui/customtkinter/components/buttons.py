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

"""Button component factories."""

from typing import Callable

import customtkinter as ctk

from backup_manager_mvp.ui.customtkinter.constants import BUTTON_HEIGHT


def create_back_button(
    parent: ctk.CTkFrame,
    command: Callable,
    width: int = 100,
) -> ctk.CTkButton:
    """Cria botão de voltar.

    Args:
        parent: Frame pai
        command: Callback do botão
        width: Largura do botão

    Returns:
        CTkButton configurado
    """
    return ctk.CTkButton(
        parent,
        text="Voltar",
        width=width,
        height=BUTTON_HEIGHT,
        command=command,
        fg_color=("gray75", "gray35"),
        hover_color=("gray65", "gray45"),
        text_color=("white", "gray95"),
        font=ctk.CTkFont(size=11, weight="bold"),
        corner_radius=6,
    )


def create_action_button(
    parent: ctk.CTkFrame,
    text: str,
    command: Callable,
    color: str = "accent_green",
    width: int | None = None,
    state: str = "normal",
) -> ctk.CTkButton:
    """Cria botão de ação genérico com hover visual adequado.

    Args:
        parent: Frame pai
        text: Texto do botão
        command: Callback
        color: Cor ("accent_green", "accent_blue", "accent_red", "gray")
        width: Largura (None = não especificar, deixar pack gerenciar)
        state: Estado ("normal" ou "disabled")

    Returns:
        CTkButton configurado
    """
    # Mapeamento color -> (fg, hover)
    color_map = {
        "accent_green": ("#00C853", "#009C3B"),
        "accent_blue": ("#0066FF", "#0052CC"),
        "accent_red": ("#FF3B30", "#E02D22"),
        "accent_orange": ("#FF9500", "#E88000"),
        "gray": (("gray75", "gray35"), ("gray65", "gray45")),
    }

    fg, hover = color_map.get(color, color_map["accent_green"])

    return ctk.CTkButton(
        parent,
        text=text,
        height=40,
        command=command,
        state=state,
        font=ctk.CTkFont(size=11, weight="bold"),
        fg_color=fg,
        hover_color=hover,
        text_color="white",
        corner_radius=6,
    )


def create_restore_button(
    parent: ctk.CTkFrame,
    command: Callable,
) -> ctk.CTkButton:
    """Cria botão de confirmação de restauração.

    Args:
        parent: Frame pai
        command: Callback

    Returns:
        CTkButton configurado
    """
    return ctk.CTkButton(
        parent,
        text="Restaurar Agora",
        command=command,
        width=120,
        height=40,
        font=ctk.CTkFont(size=11, weight="bold"),
        fg_color="#00C853",
        hover_color="#009C3B",
        text_color="white",
        corner_radius=6,
    )
