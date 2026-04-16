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

"""Button state management utilities."""

import customtkinter as ctk


def disable_buttons(
    main_window: ctk.CTk,
    backup_create_btn: ctk.CTkButton | None = None,
    sync_btn: ctk.CTkButton | None = None,
) -> None:
    """Desabilita botões de ação durante operações.

    Args:
        main_window: Janela principal
        backup_create_btn: Botão de criar backup (opcional)
        sync_btn: Botão de sincronizar (opcional)
    """
    if backup_create_btn:
        backup_create_btn.configure(state="disabled")
    if sync_btn:
        sync_btn.configure(state="disabled")
    main_window.update()


def enable_buttons(
    main_window: ctk.CTk,
    backup_create_btn: ctk.CTkButton | None = None,
    sync_btn: ctk.CTkButton | None = None,
) -> None:
    """Habilita botões de ação após operações.

    Args:
        main_window: Janela principal
        backup_create_btn: Botão de criar backup (opcional)
        sync_btn: Botão de sincronizar (opcional)
    """
    if backup_create_btn:
        backup_create_btn.configure(state="normal")
    if sync_btn:
        sync_btn.configure(state="normal")
    main_window.update()
