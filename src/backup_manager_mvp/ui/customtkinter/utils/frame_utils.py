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
