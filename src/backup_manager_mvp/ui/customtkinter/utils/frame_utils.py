# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

"""Frame manipulation utilities."""

import customtkinter as ctk


def clear_frame(
    frame: ctk.CTkFrame,
    preserve_loading: ctk.CTkLabel | None = None,
    preserve_toast: ctk.CTkLabel | None = None,
) -> None:
    """Limpa todos os widgets de um frame, preservando widgets específicos.

    Args:
        frame: Frame a limpar
        preserve_loading: Label de loading a preservar (opcional)
        preserve_toast: Label de toast a preservar (opcional)
    """
    for widget in frame.winfo_children():
        if widget is not preserve_loading and widget is not preserve_toast:
            widget.destroy()
