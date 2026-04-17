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

"""Tela 3: Confirmação de restauração."""

from collections.abc import Callable

import customtkinter as ctk

from backup_manager_mvp.models.backup_model import BackupModel
from backup_manager_mvp.models.world_model import WorldModel
from backup_manager_mvp.ui.customtkinter.components.buttons import create_restore_button
from backup_manager_mvp.ui.customtkinter.components.frames import create_separator
from backup_manager_mvp.ui.customtkinter.constants import COLORS
from backup_manager_mvp.ui.customtkinter.utils import clear_frame, hide_loading


def show_screen_restore_confirmation(
    main_frame: ctk.CTkFrame,
    world: WorldModel,
    backup: BackupModel,
    on_cancel: Callable[[], None],
    on_confirm: Callable[[BackupModel, WorldModel], None],
) -> None:
    """Exibe tela 3: Confirmação de restauração.

    Args:
        main_frame: Frame principal
        world: Mundo que será restaurado
        backup: Backup a ser restaurado
        on_cancel: Callback para cancelar
        on_confirm: Callback para confirmar restauração
    """
    hide_loading(None)
    clear_frame(main_frame)

    # === DIALOG TITLE ===
    title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    title_frame.pack(fill="x", padx=20, pady=(20, 10))

    title_label = ctk.CTkLabel(
        title_frame,
        text="Restaurar Backup - Confirmar",
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color=("gray10", "gray90"),
    )
    title_label.pack(anchor="w")

    # === DIVIDER ===
    divider = create_separator(main_frame)
    divider.pack(fill="x", padx=20, pady=10)

    # === CONTENT ===
    content_frame = ctk.CTkFrame(
        main_frame,
        fg_color=("gray95", "gray18"),
        border_width=1,
        border_color=("gray70", "gray40"),
        corner_radius=8,
    )
    content_frame.pack(fill="both", expand=True, padx=20, pady=10)

    scroll_content = ctk.CTkScrollableFrame(
        content_frame, fg_color="transparent", orientation="vertical"
    )
    scroll_content.pack(fill="both", expand=True, padx=16, pady=16)

    # === MUNDO ===
    world_label = ctk.CTkLabel(
        scroll_content,
        text=f"Mundo: {world.levelname}",
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color=("gray10", "gray90"),
        fg_color="transparent",
    )
    world_label.pack(anchor="w", pady=(0, 8))

    # === BACKUP ===
    backup_label = ctk.CTkLabel(
        scroll_content,
        text=f"Backup: {backup.name}",
        font=ctk.CTkFont(size=11),
        text_color=("gray30", "gray80"),
        fg_color="transparent",
    )
    backup_label.pack(anchor="w", pady=(0, 4))

    # === DATA ===
    date_text = backup.created_at.strftime("%d/%m/%Y %H:%M")
    date_label = ctk.CTkLabel(
        scroll_content,
        text=f"Data: {date_text}",
        font=ctk.CTkFont(size=10),
        text_color=("gray50", "gray70"),
        fg_color="transparent",
    )
    date_label.pack(anchor="w", pady=(0, 4))

    # === TAMANHO ===
    size_label = ctk.CTkLabel(
        scroll_content,
        text=f"Tamanho: {backup.size_display}",
        font=ctk.CTkFont(size=10),
        text_color=("gray50", "gray70"),
        fg_color="transparent",
    )
    size_label.pack(anchor="w", pady=(0, 16))

    # === WARNING ===
    warning_label = ctk.CTkLabel(
        scroll_content,
        text="Seus arquivos atuais serão sobrescritos.\nEsta ação não pode ser desfeita.",
        font=ctk.CTkFont(size=10, weight="bold"),
        text_color=COLORS["accent_red"],
        fg_color="transparent",
        justify="left",
    )
    warning_label.pack(anchor="w")

    # === BUTTONS ===
    buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    buttons_frame.pack(fill="x", padx=20, pady=(0, 20))

    cancel_btn = ctk.CTkButton(
        buttons_frame,
        text="Cancelar",
        command=on_cancel,
        width=120,
        height=40,
        font=ctk.CTkFont(size=11, weight="bold"),
        fg_color=("gray75", "gray35"),
        hover_color=("gray65", "gray45"),
        text_color=("white", "gray95"),
        corner_radius=6,
    )
    cancel_btn.pack(side="left", padx=(0, 10))

    restore_btn = create_restore_button(
        buttons_frame,
        on_confirm,
    )
    restore_btn.pack(side="left")
