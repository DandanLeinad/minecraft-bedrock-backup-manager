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

"""Label component factories."""

import customtkinter as ctk


def create_title_label(
    parent: ctk.CTkFrame,
    text: str,
    size: int = 16,
) -> ctk.CTkLabel:
    """Cria label de título.

    Args:
        parent: Frame pai
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
    parent: ctk.CTkFrame,
    text: str,
    size: int = 10,
) -> ctk.CTkLabel:
    """Cria label de metadados (tamanho, data, etc).

    Args:
        parent: Frame pai
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


def create_stat_label(parent: ctk.CTkFrame, text: str) -> ctk.CTkLabel:
    """Cria label de estatística.

    Args:
        parent: Frame pai
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


def create_stat_value_label(parent: ctk.CTkFrame, text: str) -> ctk.CTkLabel:
    """Cria label do valor de estatística.

    Args:
        parent: Frame pai
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
