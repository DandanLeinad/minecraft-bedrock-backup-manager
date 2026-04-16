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

"""Tela 1: Lista de mundos."""

from typing import Callable

import customtkinter as ctk

from backup_manager_mvp.models.world_model import WorldModel
from backup_manager_mvp.ui.customtkinter.components.buttons import create_action_button
from backup_manager_mvp.ui.customtkinter.components.frames import (
    create_world_item_frame,
)
from backup_manager_mvp.ui.customtkinter.components.labels import (
    create_metadata_label,
    create_title_label,
)
from backup_manager_mvp.ui.customtkinter.constants import SPACING_MEDIUM
from backup_manager_mvp.ui.customtkinter.utils import clear_frame, hide_loading


def show_screen_worlds_list(
    main_frame: ctk.CTkFrame,
    worlds: list[WorldModel],
    on_world_selected: Callable[[WorldModel], None],
    app,
) -> None:
    """Exibe tela 1: Lista de mundos.

    Args:
        main_frame: Frame principal
        worlds: Lista de mundos
        on_world_selected: Callback para seleção de mundo
        app: Referência à aplicação (para access services)
    """
    hide_loading(None)
    clear_frame(main_frame)

    # === CONTAINER COM SCROLL ===
    scroll_frame = ctk.CTkScrollableFrame(
        main_frame,
        fg_color=("gray97", "gray13"),
        orientation="vertical",
    )
    scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # === TITLE ===
    title = create_title_label(scroll_frame, "Mundos Disponíveis", size=16)
    title.pack(pady=SPACING_MEDIUM, padx=10)

    # === LISTA DE MUNDOS ===
    if not worlds:
        no_worlds = ctk.CTkLabel(
            scroll_frame,
            text="Nenhum mundo Minecraft encontrado no sistema.",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        )
        no_worlds.pack(pady=24)
    else:
        for world in worlds:
            # Calcular metadados usando o serviço
            if app and hasattr(app, "world_service"):
                metadata = app.world_service.get_world_metadata(
                    world, app.backup_service
                )
            else:
                metadata = {
                    "size": "N/A",
                    "backups_count": "0",
                    "last_backup": "Nunca",
                }

            # Factory function para criar handler com closure correto
            def make_world_handler(w: WorldModel):
                return lambda: on_world_selected(w)

            # Frame do item do mundo
            world_frame = create_world_item_frame(scroll_frame)
            world_frame.pack(fill="x", pady=10, padx=10)

            # Frame de conteúdo (esquerda) - nome e metadados
            content_frame = ctk.CTkFrame(world_frame, fg_color="transparent")
            content_frame.pack(side="left", fill="both", expand=True, padx=16, pady=12)

            # Nome do mundo
            name_label = ctk.CTkLabel(
                content_frame,
                text=world.levelname,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=("gray10", "gray95"),
                fg_color="transparent",
            )
            name_label.pack(anchor="w", pady=(0, 6))

            # Metadados
            metadata_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            metadata_frame.pack(anchor="w", pady=(0, 0), fill="x")

            # Tamanho
            size_label = create_metadata_label(metadata_frame, metadata["size"])
            size_label.pack(side="left", padx=(0, 16))

            # Backups
            backups_label = create_metadata_label(
                metadata_frame, f"{metadata['backups_count']} Backups"
            )
            backups_label.pack(side="left", padx=(0, 16))

            # Último backup
            last_backup_label = create_metadata_label(
                metadata_frame, metadata["last_backup"]
            )
            last_backup_label.pack(side="left")

            # === BOTÃO ABRIR ===
            open_btn = create_action_button(
                world_frame,
                "Abrir",
                make_world_handler(world),
                color="accent_blue",
                width=80,
            )
            open_btn.pack(side="right", padx=10, pady=8)
