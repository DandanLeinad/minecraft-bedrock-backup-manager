# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

"""Label component factories."""

from typing import Any

import customtkinter as ctk

CTkParent = Any


def create_title_label(
    parent: CTkParent,
    text: str,
    size: int = 16,
) -> ctk.CTkLabel:
    """Cria label de título.

    Args:
        parent: Widget pai (CTkFrame, CTkScrollableFrame, etc.)
        text: Texto do título
        size: Tamanho da fonte

    Returns:
        CTkLabel configurado
    """
    return ctk.CTkLabel(
        parent,
        text=text,
        font=ctk.CTkFont(size=size, weight="bold"),
        text_color=("gray10", "gray90"),
    )


def create_metadata_label(
    parent: CTkParent,
    text: str,
    size: int = 10,
) -> ctk.CTkLabel:
    """Cria label de metadados (tamanho, data, etc).

    Args:
        parent: Widget pai
        text: Texto do label
        size: Tamanho da fonte

    Returns:
        CTkLabel configurado
    """
    return ctk.CTkLabel(
        parent,
        text=text,
        font=ctk.CTkFont(size=size),
        text_color=("gray50", "gray65"),
        fg_color="transparent",
    )


def create_stat_label(parent: CTkParent, text: str) -> ctk.CTkLabel:
    """Cria label de estatística.

    Args:
        parent: Widget pai
        text: Texto do label

    Returns:
        CTkLabel configurado
    """
    return ctk.CTkLabel(
        parent,
        text=text,
        font=ctk.CTkFont(size=9),
        text_color=("gray50", "gray65"),
        fg_color="transparent",
    )


def create_stat_value_label(parent: CTkParent, text: str) -> ctk.CTkLabel:
    """Cria label do valor de estatística.

    Args:
        parent: Widget pai
        text: Valor a exibir

    Returns:
        CTkLabel configurado
    """
    return ctk.CTkLabel(
        parent,
        text=text,
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color=("gray10", "gray95"),
        fg_color="transparent",
    )
