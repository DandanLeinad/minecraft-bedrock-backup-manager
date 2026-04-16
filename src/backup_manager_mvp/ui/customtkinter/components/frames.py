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

"""Frame component factories."""

import customtkinter as ctk


def create_header_frame(parent: ctk.CTkFrame) -> ctk.CTkFrame:
    """Cria frame de header com estilo padrão.

    Args:
        parent: Frame pai

    Returns:
        CTkFrame configurado
    """
    return ctk.CTkFrame(parent, fg_color="transparent")


def create_stats_frame(parent: ctk.CTkFrame) -> ctk.CTkFrame:
    """Cria frame de estatísticas (3 colunas).

    Args:
        parent: Frame pai

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


def create_info_frame(parent: ctk.CTkFrame) -> ctk.CTkFrame:
    """Cria frame de informações (caminho, conta, etc).

    Args:
        parent: Frame pai

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


def create_separator(parent: ctk.CTkFrame, height: int = 1) -> ctk.CTkFrame:
    """Cria separador visual.

    Args:
        parent: Frame pai
        height: Altura do separador

    Returns:
        CTkFrame configurado
    """
    return ctk.CTkFrame(
        parent,
        height=height,
        fg_color=("gray70", "gray40"),
    )


def create_world_item_frame(parent: ctk.CTkFrame) -> ctk.CTkFrame:
    """Cria frame para item de mundo na lista.

    Args:
        parent: Frame pai

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


def create_backup_item_frame(parent: ctk.CTkFrame) -> ctk.CTkFrame:
    """Cria frame para item de backup na lista.

    Args:
        parent: Frame pai

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
