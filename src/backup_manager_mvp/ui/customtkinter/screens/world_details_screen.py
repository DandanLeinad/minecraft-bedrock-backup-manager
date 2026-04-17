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

"""Tela 2: Detalhes do mundo e seus backups."""

from collections.abc import Callable

import customtkinter as ctk

from backup_manager_mvp.models.backup_model import BackupModel
from backup_manager_mvp.models.world_model import WorldModel
from backup_manager_mvp.ui.customtkinter.components.buttons import (
    create_action_button,
    create_back_button,
)
from backup_manager_mvp.ui.customtkinter.components.frames import (
    create_backup_item_frame,
    create_info_frame,
    create_separator,
    create_stats_frame,
)
from backup_manager_mvp.ui.customtkinter.components.labels import (
    create_metadata_label,
    create_stat_label,
    create_stat_value_label,
    create_title_label,
)
from backup_manager_mvp.ui.customtkinter.constants import SPACING_LARGE, SPACING_MEDIUM
from backup_manager_mvp.ui.customtkinter.utils import clear_frame, hide_loading


def show_screen_world_details(
    main_frame: ctk.CTkFrame,
    world: WorldModel,
    backups: list[BackupModel],
    on_create_backup: Callable[[WorldModel], None],
    on_sync_backups: Callable[[WorldModel], None],
    on_backup_selected: Callable[[BackupModel, WorldModel], None],
    on_back: Callable[[], None],
    backup_create_btn_ref: dict,
    sync_btn_ref: dict,
    buttons_enabled: bool,
    app,
) -> None:
    """Exibe tela 2: Detalhes do mundo.

    Args:
        main_frame: Frame principal
        world: Mundo selecionado
        backups: Lista de backups
        on_create_backup: Callback para criar backup
        on_sync_backups: Callback para sincronizar
        on_backup_selected: Callback para seleção de backup
        on_back: Callback para voltar
        backup_create_btn_ref: Referência para armazenar botão (dict)
        sync_btn_ref: Referência para armazenar botão (dict)
        buttons_enabled: Se botões estão habilitados
        app: Referência à aplicação
    """
    hide_loading(None)
    clear_frame(main_frame)

    # === HEADER COM BOTÃO VOLTAR ===
    header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    header_frame.pack(fill="x", padx=10, pady=(10, 5))

    back_btn = create_back_button(header_frame, on_back)
    back_btn.pack(side="left", padx=(0, 10))

    title = create_title_label(header_frame, world.levelname, size=14)
    title.pack(side="left")

    # === STATS BOX ===
    if app and hasattr(app, "world_service"):
        metadata = app.world_service.get_world_metadata(world, app.backup_service)
    else:
        metadata = {
            "size": "N/A",
            "backups_count": "0",
            "last_backup": "Nunca",
        }

    stats_frame = create_stats_frame(main_frame)
    stats_frame.pack(fill="x", padx=10, pady=10)

    # Coluna 1: Tamanho
    stat_col1 = ctk.CTkFrame(stats_frame, fg_color="transparent")
    stat_col1.pack(side="left", fill="both", expand=True, padx=16, pady=12)
    create_stat_label(stat_col1, "Tamanho").pack()
    create_stat_value_label(stat_col1, metadata["size"]).pack(pady=(4, 0))

    # Divisor
    divider1 = ctk.CTkFrame(stats_frame, width=1, fg_color=("gray70", "gray40"))
    divider1.pack(side="left", fill="y", padx=0)

    # Coluna 2: Backups
    stat_col2 = ctk.CTkFrame(stats_frame, fg_color="transparent")
    stat_col2.pack(side="left", fill="both", expand=True, padx=16, pady=12)
    create_stat_label(stat_col2, "Backups").pack()
    create_stat_value_label(stat_col2, metadata["backups_count"]).pack(pady=(4, 0))

    # Divisor
    divider2 = ctk.CTkFrame(stats_frame, width=1, fg_color=("gray70", "gray40"))
    divider2.pack(side="left", fill="y", padx=0)

    # Coluna 3: Último Backup
    stat_col3 = ctk.CTkFrame(stats_frame, fg_color="transparent")
    stat_col3.pack(side="left", fill="both", expand=True, padx=16, pady=12)
    create_stat_label(stat_col3, "Último Backup").pack()
    create_stat_value_label(stat_col3, metadata["last_backup"]).pack(pady=(4, 0))

    # === INFORMAÇÕES ===
    info_frame = create_info_frame(main_frame)
    info_frame.pack(fill="x", padx=10, pady=10)

    path_label = ctk.CTkLabel(
        info_frame,
        text=f"Caminho: {world.path}",
        font=ctk.CTkFont(size=10),
        text_color=("gray50", "gray60"),
        wraplength=400,
        justify="left",
    )
    path_label.pack(anchor="w", padx=10, pady=(10, 5))

    account_label = ctk.CTkLabel(
        info_frame,
        text=f"Conta: {world.account_id}",
        font=ctk.CTkFont(size=10),
        text_color=("gray50", "gray60"),
    )
    account_label.pack(anchor="w", padx=10, pady=(0, 10))

    # === SEPARADOR ===
    separator = create_separator(main_frame)
    separator.pack(fill="x", padx=10, pady=5)

    # === BOTÕES DE AÇÃO ===
    buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    buttons_frame.pack(fill="x", padx=10, pady=10)

    backup_create_btn = create_action_button(
        buttons_frame,
        "Criar Backup",
        lambda: on_create_backup(world),
        color="accent_green",
        state="normal" if buttons_enabled else "disabled",
    )
    backup_create_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
    backup_create_btn_ref["button"] = backup_create_btn

    sync_btn = create_action_button(
        buttons_frame,
        "Atualizar",
        lambda: on_sync_backups(world),
        color="accent_blue",
    )
    sync_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))
    sync_btn_ref["button"] = sync_btn

    # === SCROLL AREA PARA BACKUPS ===
    scroll_frame = ctk.CTkScrollableFrame(
        main_frame,
        fg_color="transparent",
        orientation="vertical",
    )
    scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # === SEPARADOR ANTES DOS BACKUPS ===
    header_separator = create_separator(scroll_frame, height=2)
    header_separator.pack(fill="x", padx=0, pady=(0, SPACING_MEDIUM))

    # === BACKUPS TITLE ===
    title_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    title_frame.pack(fill="x", pady=(0, SPACING_MEDIUM), padx=10)

    backups_title = create_title_label(title_frame, "Backups Disponíveis", size=13)
    backups_title.pack(anchor="w")

    # === LISTA DE BACKUPS ===
    if not backups:
        no_backups = ctk.CTkLabel(
            scroll_frame,
            text="Nenhum backup encontrado para este mundo.",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        )
        no_backups.pack(pady=SPACING_LARGE)
    else:
        for backup in backups:

            def make_backup_handler(b: BackupModel):
                return lambda: on_backup_selected(b, world)

            # Frame do backup
            backup_frame = create_backup_item_frame(scroll_frame)
            backup_frame.pack(fill="x", pady=8, padx=10)

            # Frame de conteúdo
            content_frame = ctk.CTkFrame(backup_frame, fg_color="transparent")
            content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=8)

            # Nome
            name_label = ctk.CTkLabel(
                content_frame,
                text=backup.name,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=("gray10", "gray90"),
                fg_color="transparent",
            )
            name_label.pack(anchor="w", pady=(0, 4))

            # Data + Tamanho
            info_frame_backup = ctk.CTkFrame(content_frame, fg_color="transparent")
            info_frame_backup.pack(fill="x", pady=(0, 0))

            date_text = backup.created_at.strftime("%d/%m/%Y %H:%M")
            create_metadata_label(info_frame_backup, f"📅 {date_text}").pack(
                side="left", padx=(0, 12)
            )

            # Separador
            sep = ctk.CTkLabel(
                info_frame_backup,
                text="│",
                font=ctk.CTkFont(size=9),
                text_color=("gray70", "gray45"),
                fg_color="transparent",
            )
            sep.pack(side="left", padx=(0, 12))

            create_metadata_label(info_frame_backup, f"📊 {backup.size_display}").pack(side="left")

            # === BOTÃO RESTAURAR ===
            restore_btn = create_action_button(
                backup_frame,
                "📥  Restaurar",
                make_backup_handler(backup),
                color="accent_blue",
                width=100,
            )
            restore_btn.pack(side="right", padx=10, pady=8)
