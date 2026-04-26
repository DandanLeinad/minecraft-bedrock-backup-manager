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

"""Tela de Preview: Mostra conteúdo do backup antes de restaurar - MC-3 FF_RESTORE_PREVIEW."""

from collections.abc import Callable

import customtkinter as ctk

from backup_manager_mvp.core.models.backup_model import BackupModel
from backup_manager_mvp.core.models.world_model import WorldModel
from backup_manager_mvp.ui.customtkinter.components.frames import create_separator
from backup_manager_mvp.ui.customtkinter.constants import COLORS
from backup_manager_mvp.ui.customtkinter.utils import clear_frame, hide_loading


def _format_size(size_bytes: int) -> str:
    """Formata bytes em string legível (B, KB, MB, GB)."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / 1024 / 1024:.1f} MB"
    else:
        return f"{size_bytes / 1024 / 1024 / 1024:.2f} GB"


def show_screen_restore_preview(
    main_frame: ctk.CTkFrame,
    world: WorldModel,
    backup: BackupModel,
    preview_info: dict,
    on_cancel: Callable[[], None],
    on_confirm: Callable[[], None],
) -> None:
    """Exibe tela de preview: Conteúdo do backup antes de restaurar.

    Args:
        main_frame: Frame principal
        world: Mundo que será restaurado
        backup: Backup a ser restaurado
        preview_info: Dicionário retornado por BackupService.get_backup_preview_info()
        on_cancel: Callback para cancelar (sem argumentos)
        on_confirm: Callback para confirmar restauração (sem argumentos - backup/world já estão em escopo)
    """
    hide_loading(None)
    clear_frame(main_frame)

    # === HEADER ===
    header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    header_frame.pack(fill="x", padx=20, pady=(20, 10))

    title_label = ctk.CTkLabel(
        header_frame,
        text="Preview do Backup - Restaurar Mundo",
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color=("gray10", "gray90"),
    )
    title_label.pack(anchor="w")

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
        text=f"🌍 Mundo: {world.levelname}",
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color=("gray10", "gray90"),
        fg_color="transparent",
    )
    world_label.pack(anchor="w", pady=(0, 4))

    # === DATA DO BACKUP ===
    date_text = backup.created_at.strftime("%d/%m/%Y %H:%M")
    date_label = ctk.CTkLabel(
        scroll_content,
        text=f"📅 Data: {date_text}",
        font=ctk.CTkFont(size=10),
        text_color=("gray50", "gray70"),
        fg_color="transparent",
    )
    date_label.pack(anchor="w", pady=(0, 12))

    # === ESTATÍSTICAS ===
    stats_frame = ctk.CTkFrame(
        scroll_content,
        fg_color=("gray85", "gray25"),
        corner_radius=6,
    )
    stats_frame.pack(fill="x", pady=(0, 16))

    # Total de arquivos
    files_text = f"📄 Arquivos: {preview_info['total_files']}"
    files_label = ctk.CTkLabel(
        stats_frame,
        text=files_text,
        font=ctk.CTkFont(size=10),
        text_color=("gray30", "gray80"),
        fg_color="transparent",
    )
    files_label.pack(anchor="w", padx=12, pady=(8, 4))

    # Total de diretórios
    dirs_text = f"📁 Pastas: {preview_info['total_dirs']}"
    dirs_label = ctk.CTkLabel(
        stats_frame,
        text=dirs_text,
        font=ctk.CTkFont(size=10),
        text_color=("gray30", "gray80"),
        fg_color="transparent",
    )
    dirs_label.pack(anchor="w", padx=12, pady=(0, 4))

    # Tamanho total
    size_formatted = _format_size(preview_info["total_size"])
    size_text = f"💾 Tamanho Total: {size_formatted}"
    size_label = ctk.CTkLabel(
        stats_frame,
        text=size_text,
        font=ctk.CTkFont(size=10, weight="bold"),
        text_color=("gray10", "gray90"),
        fg_color="transparent",
    )
    size_label.pack(anchor="w", padx=12, pady=(0, 8))

    # === CONTEÚDO DO BACKUP ===
    if preview_info["error"] is None and preview_info["top_level_items"]:
        content_label = ctk.CTkLabel(
            scroll_content,
            text="Conteúdo do Backup:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("gray10", "gray90"),
            fg_color="transparent",
        )
        content_label.pack(anchor="w", pady=(8, 8))

        # Lista de itens
        for item in preview_info["top_level_items"]:
            item_frame = ctk.CTkFrame(
                scroll_content,
                fg_color=("gray92", "gray22"),
                corner_radius=4,
            )
            item_frame.pack(fill="x", pady=2)

            # Ícone + nome
            icon = "📁" if item["type"] == "dir" else "📄"
            if item["type"] == "ellipsis":
                icon = "⋯"

            item_text = f"{icon} {item['name']}"
            item_name_label = ctk.CTkLabel(
                item_frame,
                text=item_text,
                font=ctk.CTkFont(size=9),
                text_color=("gray20", "gray80"),
                fg_color="transparent",
            )
            item_name_label.pack(anchor="w", padx=8, pady=4)

            # Tamanho (se não for ellipsis)
            if item["type"] != "ellipsis" and item["size"] > 0:
                size_text = _format_size(item["size"])
                item_size_label = ctk.CTkLabel(
                    item_frame,
                    text=f"  {size_text}",
                    font=ctk.CTkFont(size=8),
                    text_color=("gray50", "gray70"),
                    fg_color="transparent",
                )
                item_size_label.pack(anchor="w", padx=8, pady=(0, 4))
    elif preview_info["error"]:
        error_label = ctk.CTkLabel(
            scroll_content,
            text=f"⚠️ Erro ao carregar preview:\n{preview_info['error']}",
            font=ctk.CTkFont(size=10),
            text_color=COLORS["accent_red"],
            fg_color="transparent",
            justify="left",
        )
        error_label.pack(anchor="w", pady=8)

    # === WARNING ===
    warning_frame = ctk.CTkFrame(
        scroll_content,
        fg_color=("gray92", "gray22"),
        corner_radius=6,
    )
    warning_frame.pack(fill="x", pady=(16, 0))

    warning_label = ctk.CTkLabel(
        warning_frame,
        text="⚠️ Seus arquivos atuais serão sobrescritos.\nEsta ação não pode ser desfeita.",
        font=ctk.CTkFont(size=10, weight="bold"),
        text_color=COLORS["accent_red"],
        fg_color="transparent",
        justify="left",
    )
    warning_label.pack(anchor="w", padx=12, pady=12)

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

    restore_btn = ctk.CTkButton(
        buttons_frame,
        text="Restaurar Agora",
        command=on_confirm,  # on_confirm já tem backup/world no escopo
        width=140,
        height=40,
        font=ctk.CTkFont(size=11, weight="bold"),
        fg_color=COLORS["accent_red"],
        hover_color=COLORS["accent_red_hover"],
        text_color="white",
        corner_radius=6,
    )
    restore_btn.pack(side="left")
