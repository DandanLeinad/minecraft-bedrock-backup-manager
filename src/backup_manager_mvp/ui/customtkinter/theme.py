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

"""Configuração de tema CustomTkinter.

Responsável por:
- Configurar modo de aparência (System, Dark, Light)
- Configurar tema de cores padrão
"""

import customtkinter as ctk


def configure_theme(appearance_mode: str = "System", color_theme: str = "blue") -> None:
    """Configura o tema da aplicação CustomTkinter.

    Args:
        appearance_mode: "System", "Dark" ou "Light"
        color_theme: "blue", "green", "dark-blue", etc.
    """
    ctk.set_appearance_mode(appearance_mode)
    ctk.set_default_color_theme(color_theme)
