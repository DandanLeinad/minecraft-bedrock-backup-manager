# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

"""Componentes reutilizáveis para UI CustomTkinter."""

from backup_manager_mvp.ui.customtkinter.components.buttons import (
    create_action_button,
    create_back_button,
    create_restore_button,
)
from backup_manager_mvp.ui.customtkinter.components.dialogs import (
    show_disclaimer_dialog,
)
from backup_manager_mvp.ui.customtkinter.components.frames import (
    create_header_frame,
    create_info_frame,
    create_stats_frame,
)
from backup_manager_mvp.ui.customtkinter.components.labels import (
    create_metadata_label,
    create_title_label,
)

__all__ = [
    "create_action_button",
    "create_back_button",
    "create_header_frame",
    "create_info_frame",
    "create_metadata_label",
    "create_restore_button",
    "create_stats_frame",
    "create_title_label",
    "show_disclaimer_dialog",
]
