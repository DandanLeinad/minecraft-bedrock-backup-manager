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
    "show_disclaimer_dialog",
    "create_action_button",
    "create_back_button",
    "create_restore_button",
    "create_header_frame",
    "create_stats_frame",
    "create_info_frame",
    "create_title_label",
    "create_metadata_label",
]
