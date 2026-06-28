# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

"""Toast notification utilities."""

import logging

import customtkinter as ctk

from backup_manager_mvp.ui.customtkinter.constants import COLORS

logger = logging.getLogger(__name__)


def show_toast(
    main_frame: ctk.CTkFrame,
    main_window: ctk.CTk,
    toast_label: ctk.CTkLabel | None,
    message: str,
    success: bool = True,
    duration: int = 2000,
) -> ctk.CTkLabel:
    """Exibe toast notification temporal.

    Args:
        main_frame: Frame pai para o toast
        main_window: Janela principal para scheduling
        toast_label: Label existente (pode ser None)
        message: Mensagem a exibir
        success: True para verde (sucesso), False para vermelho (erro)
        duration: Duração em ms

    Returns:
        Label do toast (para reutilização)
    """
    # Verificar se widget ainda existe
    if toast_label and toast_label.winfo_exists():
        toast_label.configure(
            text=message,
            fg_color=COLORS["accent_green"] if success else COLORS["accent_red"],
        )
        toast_label.pack(pady=10, padx=10)
    else:
        # Recriar se foi destruído
        toast_label = ctk.CTkLabel(
            main_frame,
            text=message,
            font=ctk.CTkFont(size=11),
            text_color="#FFFFFF",
            fg_color=COLORS["accent_green"] if success else COLORS["accent_red"],
            corner_radius=6,
        )
        toast_label.pack(pady=10, padx=10)

    main_window.update()
    # Auto-hide após duration
    main_window.after(duration, lambda: hide_toast(toast_label))
    return toast_label


def hide_toast(toast_label: ctk.CTkLabel | None) -> None:
    """Esconde toast.

    Args:
        toast_label: Label do toast a esconder
    """
    if toast_label and toast_label.winfo_exists():
        toast_label.pack_forget()
