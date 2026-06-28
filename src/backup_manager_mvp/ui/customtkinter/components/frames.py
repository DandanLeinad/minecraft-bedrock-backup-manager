# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

"""Frame component factories."""

from typing import Any

import customtkinter as ctk

# Type alias for any widget that can be a parent (CTkFrame, CTkScrollableFrame, etc.)
CTkParent = Any


def create_header_frame(parent: CTkParent) -> ctk.CTkFrame:
    """Cria frame de header com estilo padrão.

    Args:
        parent: Widget pai (CTkFrame, CTkScrollableFrame, etc.)

    Returns:
        CTkFrame configurado
    """
    return ctk.CTkFrame(parent, fg_color="transparent")


def create_stats_frame(parent: CTkParent) -> ctk.CTkFrame:
    """Cria frame de estatísticas (3 colunas).

    Args:
        parent: Widget pai

    Returns:
        CTkFrame configurado
    """
    return ctk.CTkFrame(
        parent,
        fg_color=("gray88", "gray25"),
        border_width=2,
        border_color=("gray70", "gray45"),
        corner_radius=8,
    )


def create_info_frame(parent: CTkParent) -> ctk.CTkFrame:
    """Cria frame de informações (caminho, conta, etc).

    Args:
        parent: Widget pai

    Returns:
        CTkFrame configurado
    """
    return ctk.CTkFrame(
        parent,
        fg_color=("gray95", "gray20"),
        border_width=1,
        border_color=("gray70", "gray40"),
        corner_radius=5,
    )


def create_separator(parent: CTkParent, height: int = 1) -> ctk.CTkFrame:
    """Cria separador visual.

    Args:
        parent: Widget pai
        height: Altura do separador

    Returns:
        CTkFrame configurado
    """
    return ctk.CTkFrame(
        parent,
        height=height,
        fg_color=("gray70", "gray40"),
    )


def create_world_item_frame(parent: CTkParent) -> ctk.CTkFrame:
    """Cria frame para item de mundo na lista.

    Args:
        parent: Widget pai

    Returns:
        CTkFrame configurado
    """
    return ctk.CTkFrame(
        parent,
        fg_color=("gray95", "gray20"),
        border_width=2,
        border_color=("gray75", "gray45"),
        corner_radius=8,
    )


def create_backup_item_frame(parent: CTkParent) -> ctk.CTkFrame:
    """Cria frame para item de backup na lista.

    Args:
        parent: Widget pai

    Returns:
        CTkFrame configurado
    """
    return ctk.CTkFrame(
        parent,
        fg_color=("gray95", "gray20"),
        border_width=2,
        border_color=("gray75", "gray45"),
        corner_radius=7,
    )
