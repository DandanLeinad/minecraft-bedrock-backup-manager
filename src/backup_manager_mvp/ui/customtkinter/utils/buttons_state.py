# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

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
